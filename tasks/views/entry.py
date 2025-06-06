# tasks/views/entry.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta

from strategy.models import Strategy
from activity.models import DailyStandardActivity
from touchlog.models import TouchLog
from tasks.forms import TouchForm
from customers.models import Customer
from tasks.constants import STEP_SEQUENCE, TOUCH_NEXT_MAP, DAILY_KPI_FIELDS

@login_required
def task_entry_view(request):
    today = now().date()
    user = request.user

    kpi_instance, _ = DailyStandardActivity.objects.get_or_create(user=user, date=today)
    strategy = Strategy.objects.filter(user=user, year=today.year, month=today.month).first()

    touch_form = TouchForm(request.POST if 'save_touch' in request.POST else None)
    if request.method == 'POST' and 'save_touch' in request.POST and touch_form.is_valid():
        touch = touch_form.save(commit=False)
        touch.user = user
        touch.save()
        messages.success(request, "✅ 고객 접촉 기록이 저장되었습니다.")
        return redirect('tasks:entry')

    active, step = request.GET.get("active"), request.GET.get("step")
    touch_tasks = get_touch_task_list(user, active=active, step=step)

    completed_steps_map, step_index_map = build_completed_step_map(touch_tasks)

    context = {
        'touch_form': touch_form,
        'strategy': strategy,
        'daily_progress_cards': set_daily_kpi_progress(strategy, kpi_instance) if strategy else [],
        'weekly_progress_cards': get_weekly_kpi_progress(user, strategy) if strategy else [],
        'kpi_history': DailyStandardActivity.objects.filter(user=user).exclude(date=today).order_by('-date')[:7],
        'touch_history': TouchLog.objects.filter(user=user).order_by('-created_at')[:7],
        'touch_tasks': touch_tasks,
        'step_choices': TOUCH_NEXT_MAP,
        'next_step_map': TOUCH_NEXT_MAP,
        'step_sequence': STEP_SEQUENCE,
        'completed_steps_map': completed_steps_map,
        'step_index_map': step_index_map,
    }
    return render(request, 'tasks/form.html', context)

def set_daily_kpi_progress(strategy, actual):
    result = []
    for label, field in DAILY_KPI_FIELDS:
        target = getattr(strategy, field, 0)
        value = getattr(actual, field, 0)
        percent = round((value / target) * 100) if target > 0 else 0
        css = "bg-green-500" if percent >= 100 else "bg-yellow-400" if percent >= 50 else "bg-red-400"
        result.append({"label": label, "field": field, "value": value, "target": target, "percent": min(percent, 100), "css": css})
    return result

def get_weekly_kpi_progress(user, strategy):
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    queryset = DailyStandardActivity.objects.filter(user=user, date__range=(start_of_week, end_of_week))
    total = {field: 0 for _, field in DAILY_KPI_FIELDS}

    for record in queryset:
        for _, field in DAILY_KPI_FIELDS:
            total[field] += getattr(record, field, 0)

    result = []
    for label, field in DAILY_KPI_FIELDS:
        value = total[field]
        weekly_target = getattr(strategy, f"weekly_{field.replace('daily_', '')}", 0)
        percent = int((value / weekly_target) * 100) if weekly_target else 0
        css = "bg-green-500" if percent >= 100 else "bg-yellow-400" if percent >= 60 else "bg-red-400"
        result.append({"label": label, "value": value, "target": weekly_target, "percent": percent, "css": css})
    return result

def get_touch_task_list(user, active=None, step=None):
    qs = Customer.objects.filter(user=user)
    if active == "1":
        qs = qs.filter(is_active_touching=True)
    elif active == "0":
        qs = qs.filter(is_active_touching=False)
    if step:
        qs = qs.filter(current_touch_step=step)
    return qs

def build_completed_step_map(touch_tasks):
    step_index_map = {}
    completed_steps_map = {}

    for c in touch_tasks:
        if c.current_touch_step:
            try:
                current_index = [s for s, _ in STEP_SEQUENCE].index(c.current_touch_step)
            except ValueError:
                current_index = -1

            step_index_map[c.id] = current_index
            completed_steps_map[c.id] = [s for i, (s, _) in enumerate(STEP_SEQUENCE) if i < current_index]

    return completed_steps_map, step_index_map