# tasks/views/adjust.py

from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from activity.models import DailyStandardActivity
from customers.models import Customer
from touchlog.models import TouchLog

@require_POST
@login_required
def adjust_kpi_view(request):
    field = request.POST.get("field")
    direction = request.POST.get("adjustment")

    print("field:", field)
    today = timezone.now().date()

    kpi, _ = DailyStandardActivity.objects.get_or_create(user=request.user, date=today)

    ALLOWED_FIELDS = [
        "daily_call_1min", "daily_call_2min", "daily_proposals",
        "daily_visit_proposals", "daily_grade_potential", "daily_band_verified"
    ]

    print(f"🛠 field={field}, dir={direction}, user={request.user.username}")
    if field in ALLOWED_FIELDS:
        current = getattr(kpi, field, 0)
        if direction == "up":
            setattr(kpi, field, current + 1)
        elif direction == "down" and current > 0:
            setattr(kpi, field, current - 1)
        kpi.save()


    return redirect("tasks:entry")

    
TOUCH_STEP_SEQUENCE = ["report", "pre_sms", "call1", "reject_sms", "call2", "visit", "done"]

@require_POST
@login_required
def advance_touch_action_view(request):
    customer_id = request.POST.get("customer_id")
    try:
        customer = Customer.objects.get(id=customer_id, user=request.user)
    except Customer.DoesNotExist:
        return redirect("tasks:entry")

    try:
        index = TOUCH_STEP_SEQUENCE.index(customer.current_touch_step)
        next_step = TOUCH_STEP_SEQUENCE[index + 1] if index + 1 < len(TOUCH_STEP_SEQUENCE) else "done"
    except ValueError:
        next_step = "done"

    customer.current_touch_step = next_step
    # 자동 비활성화 삭제: is_active_touching 건드리지 않음
    customer.save()

    TouchLog.objects.create(
        user=request.user,
        customer=customer,
        method="system",
        memo=f"[자동] {customer.get_current_touch_step_display()} 진행 처리",
        is_auto=True
    )

    return redirect("tasks:entry")


@require_POST
@login_required
def revert_touch_action_view(request):
    customer_id = request.POST.get("customer_id")
    try:
        customer = Customer.objects.get(id=customer_id, user=request.user)
    except Customer.DoesNotExist:
        return redirect("tasks:entry")

    try:
        index = TOUCH_STEP_SEQUENCE.index(customer.current_touch_step)
        prev_step = TOUCH_STEP_SEQUENCE[index - 1] if index > 0 else "report"
    except ValueError:
        prev_step = "report"

    customer.current_touch_step = prev_step
    customer.is_active_touching = True  # 강제 활성화
    customer.save()

    TouchLog.objects.create(
        user=request.user,
        customer=customer,
        method="system",
        memo=f"[자동] {customer.get_current_touch_step_display()} 단계로 되돌림",
        is_auto=True
    )

    return redirect("tasks:entry")


@require_POST
@login_required
def complete_touch_action_view(request):
    customer_id = request.POST.get("customer_id")
    try:
        customer = Customer.objects.get(id=customer_id, user=request.user)
    except Customer.DoesNotExist:
        return redirect("tasks:entry")

    # 수동 완료 처리: is_active_touching = False
    customer.is_active_touching = False
    customer.save()

    TouchLog.objects.create(
        user=request.user,
        customer=customer,
        method="system",
        memo="[수동] 고객 접촉 완료 처리",
        is_auto=True
    )

    return redirect("tasks:entry")