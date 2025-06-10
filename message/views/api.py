# message/views/api.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import now
from message.models import MessageQueue, RecipientStatus
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
import json

# 임시 저장소 (메모리 캐시 또는 DB로 교체 가능)
from django.core.cache import cache

User = get_user_model()


@csrf_exempt
def launcher_ping(request):
    status = request.GET.get("installed")
    if status not in ["yes", "no"]:
        return JsonResponse({"error": "Invalid status"}, status=400)

    # 임시 저장 (10초 TTL)
    cache.set("launcher_ping_status", {
        "installed": status,
        "timestamp": now().isoformat()
    }, timeout=10)

    return JsonResponse({"result": "ok", "installed": status})

def launcher_ping_latest(request):
    data = cache.get("launcher_ping_status", None)
    if data is None:
        return JsonResponse({"installed": "unknown", "timestamp": None})
    return JsonResponse(data)

@csrf_exempt
@require_POST
def lock_and_fetch_messages(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        limit = int(data.get("limit", 5))

        if not user_id:
            return JsonResponse({"status": "error", "message": "user_id 누락"}, status=400)

        with transaction.atomic():
            msgs = (
                MessageQueue.objects
                .select_for_update(skip_locked=True)
                .filter(user_id=user_id, status="pending")
                .order_by("created_at")[:limit]
            )

            msg_list = list(msgs)

            for m in msg_list:
                m.status = "locked"
                m.save()

        result = [
            {
                "id": m.id,
                "recipients": [
                   {"name": c.name, "customer_id": c.id}
                   for c in m.recipients.all()
                ],
                "message": m.message,
                "image_url": m.image_url,
                "created_at": m.created_at.isoformat()
            }
            for m in msg_list
        ]

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
@csrf_exempt
@require_POST
def report_message_status(request):
    try:
        data = json.loads(request.body)
        msg_id = data.get("id")
        customer_id = data.get("customer_id")

        status = data.get("status")
        step_log = data.get("step_log", [])
        reason = json.dumps(step_log, ensure_ascii=False, indent=2)

        print(f"[🧪 DEBUG] message_id={msg_id}, customer_id={customer_id}, status={status}")

        if not msg_id or not customer_id or status not in ["sent", "failed"]:
            return JsonResponse({"status": "error", "message": "필드 누락"}, status=400)

        mq = get_object_or_404(MessageQueue, id=msg_id)
        rs = RecipientStatus.objects.filter(message=mq, customer_id=customer_id).first()
        if not rs:
            return JsonResponse({"status": "error", "message": "RecipientStatus 없음"}, status=404)

        rs.status = status
        rs.reason = reason
        if status == "sent":
            rs.sent_at = now()
        rs.save()

        return JsonResponse({"status": "success"})

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@require_GET
def recipient_status_list(request):
    user_id = request.GET.get("user_id")
    message_id = request.GET.get("message_id")

    try:
        if not user_id:
            return JsonResponse({"error": "user_id required"}, status=400)

        from message.models import RecipientStatus

        filters = {"message__user_id": user_id}
        if message_id and message_id != "latest":
            filters["message_id"] = message_id
        elif message_id == "latest":
            latest = (
                RecipientStatus.objects
                .filter(message__user_id=user_id)
                .order_by("-created_at")
                .first()
            )
            if latest:
                filters["message_id"] = latest.message.id
            else:
                return JsonResponse([], safe=False)

        statuses = (
            RecipientStatus.objects
            .filter(**filters)
            .select_related("customer")
            .order_by("created_at")
        )

        data = [{
            "customer_id": s.customer.id,
            "name": s.customer.name,
            "status": s.status,
            "reason": s.reason or ""
        } for s in statuses]

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


        
@require_GET
@ensure_csrf_cookie
def message_status_summary(request):
    user = request.user
    total = MessageQueue.objects.filter(user=user).count()
    sent = MessageQueue.objects.filter(user=user, status="sent").count()
    failed = MessageQueue.objects.filter(user=user, status="failed").count()
    pending = MessageQueue.objects.filter(user=user, status="pending").count()
    locked = MessageQueue.objects.filter(user=user, status="locked").count()

    return JsonResponse({
        "total": total,
        "sent": sent,
        "failed": failed,
        "pending": pending,
        "locked": locked,
        "completed": sent + failed
    })

@csrf_exempt
def sender_shutdown_view(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return JsonResponse({"status": "error", "message": "user_id required"}, status=400)

    # 10초 동안 유효한 종료 요청 플래그 저장
    cache.set(f"sender_shutdown_flag:{user_id}", {"time": now().isoformat()}, timeout=10)
    return JsonResponse({"status": "ok", "message": "shutdown flag set"})