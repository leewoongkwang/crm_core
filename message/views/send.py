
# message/views/send.py
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from message.models import MessageQueue
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from customers.models import Customer

@login_required
@require_http_methods(["GET", "POST"])
def send_message_view(request):
    if request.method == "POST":
        try:
            recipients = list(map(int, request.POST.getlist("recipients")))
        except ValueError:
            recipients = []

        message = request.POST.get("message")
        image_url = request.POST.get("image_url", None)

        if not recipients or not message:
            messages.error(request, "❌ 수신자와 메시지는 필수입니다.")
            customers = Customer.objects.filter(user=request.user).order_by("-created_at")
            return render(request, "message/send_form.html", {
                "customers": customers,
            }, status=400)

        from django.db import transaction
        with transaction.atomic():
            mq = MessageQueue.objects.create(
                user=request.user,
                message=message,
                image_url=image_url or None,
                status="pending",
            )
            mq.recipients.set(Customer.objects.filter(id__in=recipients))

        messages.success(request, "✅ 메시지 전송 요청이 등록되었습니다.")
        return redirect("message:send")

    # GET 요청
    customers = Customer.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "message/send_form.html", {
        "customers": customers
    })

@csrf_exempt
def sender_ping_view(request):
    user_id = request.GET.get("user_id")
    status = request.GET.get("status")

    if user_id and status == "running":
        cache.set(f"sender_running_{user_id}", True, timeout=30)  # 30초간 실행 중으로 기록
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False})