from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now

from strategy.models import Strategy
from activity.models import DailyStandardActivity
from touchlog.models import TouchLog
from tasks.forms import KPIForm, TouchForm

@login_required
def task_entry_view(request):
    today = now().date()

    # KPI 실적 객체 생성/조회
    kpi_instance, _ = DailyStandardActivity.objects.get_or_create(user=request.user, date=today)
    kpi_form = KPIForm(request.POST or None, instance=kpi_instance)

    # 전략값 로드 (year + month 기준)
    strategy = Strategy.objects.filter(
        user=request.user, year=today.year, month=today.month
    ).first()

    # 고객 접촉 기록 폼 (빈 인스턴스)
    touch_form = TouchForm(request.POST or None)

    if request.method == 'POST':
        if 'save_kpi' in request.POST and kpi_form.is_valid():
            kpi = kpi_form.save(commit=False)
            kpi.user = request.user
            kpi.date = today
            kpi.save()
            messages.success(request, "✅ 오늘의 KPI 실적이 저장되었습니다.")
            return redirect('tasks:entry')

        elif 'save_touch' in request.POST and touch_form.is_valid():
            touch = touch_form.save(commit=False)
            touch.user = request.user
            touch.save()
            messages.success(request, "✅ 고객 접촉 기록이 저장되었습니다.")
            return redirect('tasks:entry')

    # KPI 이력: 최근 7일
    kpi_history = DailyStandardActivity.objects.filter(
        user=request.user
    ).exclude(date=today).order_by('-date')[:7]

    # 고객 접촉 이력: 최근 7건
    touch_history = TouchLog.objects.filter(user=request.user).order_by('-created_at')[:7]

    progress_cards = calculate_progress(strategy, kpi_instance) if strategy else []

    return render(request, 'tasks/form.html', {
        'kpi_form': kpi_form,
        'touch_form': touch_form,
        'kpi_history': kpi_history,
        'touch_history': touch_history,
        'strategy': strategy,
        'progress_cards': progress_cards,  
    })

def calculate_progress(strategy, actual):
    progress = []
    fields = [
        ("1분콜", "daily_call_1min"),
        ("2분콜", "daily_call_2min"),
        ("고객 제안", "daily_proposals"),
        ("방문 제안", "daily_visit_proposals"),
        ("가망 확보", "daily_grade_potential"),
        ("밴드 인증", "daily_band_verified"),
    ]

    for label, field in fields:
        target = getattr(strategy, field, 0)
        value = getattr(actual, field, 0)
        percent = round((value / target) * 100) if target > 0 else 0
        progress.append({
            "label": label,
            "value": value,
            "target": target,
            "percent": percent,
            "css": "bg-yellow-500" if percent >= 100 else "bg-red-500",
        })

    return progress
