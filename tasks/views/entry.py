from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from datetime import date, timedelta
from strategy.models import Strategy
from activity.models import DailyStandardActivity
from touchlog.models import TouchLog
from tasks.forms import TouchForm
from customers.models import Customer

@login_required
def task_entry_view(request):
    today = now().date()

    # KPI 실적 객체 생성/조회
    kpi_instance, _ = DailyStandardActivity.objects.get_or_create(user=request.user, date=today)

    # 전략값 로드 (year + month 기준)
    strategy = Strategy.objects.filter(
        user=request.user, year=today.year, month=today.month
    ).first()

    # 고객 접촉 기록 폼 (빈 인스턴스)
    touch_form = TouchForm(request.POST if 'save_touch' in request.POST else None)

    if request.method == 'POST':
        if 'save_touch' in request.POST and touch_form.is_valid():
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
    weekly_progress_cards = get_weekly_kpi_progress(request.user)
    touch_tasks = get_touch_task_list(request.user)

    # 터치 단계 시퀀스 (순서 보장)
    step_sequence = [
        ("report", "리포트"),
        ("pre_sms", "콜 전 문자"),
        ("call1", "1차 콜"),
        ("reject_sms", "거절 후 제안"),
        ("call2", "2차 콜"),
        ("visit", "방문 제안"),
        ("done", "완료"),
    ]
    return render(request, 'tasks/form.html', {
        'touch_form': touch_form,
        'kpi_history': kpi_history,
        'touch_history': touch_history,
        'strategy': strategy,
        'progress_cards': progress_cards,
        'weekly_progress_cards': weekly_progress_cards,  
        'touch_tasks': touch_tasks,
        'next_step_map': TOUCH_NEXT_MAP,
        'step_sequence': step_sequence,
        'completed_steps_map': {
            c.id: [
                s for s, _ in step_sequence
                if step_sequence.index((s, _)) < step_sequence.index((c.current_touch_step, dict(step_sequence)[c.current_touch_step]))
            ] for c in touch_tasks
        },
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
        percent = min(percent, 100)

        progress.append({
            "label": label,
            "field": field,  # ⬅️ 버튼용 필드명 포함
            "value": value,
            "target": target,
            "percent": percent,
            "css": "bg-green-500" if percent >= 100 else ("bg-yellow-400" if percent >= 50 else "bg-red-400"),
        })

    return progress

def get_weekly_kpi_progress(user):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # 월요일
    end_of_week = start_of_week + timedelta(days=6)

    # 전략 목표
    try:
        strategy = Strategy.objects.get(user=user, year=today.year, month=today.month)
    except Strategy.DoesNotExist:
        return []

    # 이번 주 KPI 누적 합계
    queryset = DailyStandardActivity.objects.filter(
        user=user, date__range=(start_of_week, end_of_week)
    )

    agg_fields = [
        "daily_call_1min", "daily_call_2min",
        "daily_proposals", "daily_visit_proposals",
        "daily_grade_potential", "daily_band_verified"
    ]
    total = {f: 0 for f in agg_fields}

    for record in queryset:
        for field in agg_fields:
            total[field] += getattr(record, field, 0)

    # 카드 생성
    card_data = []
    for field in agg_fields:
        label = {
            "daily_call_1min": "1분콜",
            "daily_call_2min": "2분콜",
            "daily_proposals": "제안",
            "daily_visit_proposals": "방문제안",
            "daily_grade_potential": "가망확보",
            "daily_band_verified": "밴드인증"
        }[field]

        value = total[field]
        weekly_target = getattr(strategy, f"weekly_{field.replace('daily_', '')}", 0)
        percent = int((value / weekly_target) * 100) if weekly_target else 0
        css = "bg-blue-500" if percent >= 100 else "bg-yellow-400" if percent >= 60 else "bg-red-400"

        card_data.append({
            "label": label,
            "value": value,
            "target": weekly_target,
            "percent": percent,
            "css": css,
        })

    return card_data


TOUCH_NEXT_MAP = {
    "report": "리포트 발송",
    "pre_sms": "1차콜 문자",
    "call1": "1차 콜",
    "reject_sms": "제안서 재전송",
    "call2": "2차 콜",
    "visit": "방문 제안",
    "done": "완료",
}

def get_touch_task_list(user):
    return Customer.objects.filter(
        user=user,
        is_active_touching=True
    ).exclude(current_touch_step="done")