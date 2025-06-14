from django.db import models
from customers.models import Customer  # 추가
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageQueue(models.Model):
    STATUS_CHOICES = (
        ("pending", "대기중"),
        ("locked", "전송중"),
        ("sent", "전송완료"),
        ("failed", "전송실패"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Customer)  # ✅ 수정
    message = models.TextField()
    image_url = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    failure_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} → {self.recipients.count()}명 ({self.status})"

class RecipientStatus(models.Model):
    message = models.ForeignKey(MessageQueue, on_delete=models.CASCADE, related_name="recipient_statuses")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=16, choices=[
        ("pending", "대기"),
        ("sent", "성공"),
        ("failed", "실패")
    ], default="pending")
    reason = models.TextField(blank=True, null=True)  # 실패 이유 or 단계 로그
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.status}"