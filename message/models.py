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