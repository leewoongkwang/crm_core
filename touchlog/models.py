from django.db import models
from customers.models import Customer
from django.contrib.auth import get_user_model
User = get_user_model()

class TouchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # 접촉 방식 (전화, 카카오, 방문 등)
    method = models.CharField(
        max_length=20,
        choices=[
            ("call", "전화"),
            ("sms", "문자"),
            ("kakao", "카카오"),
            ("visit", "방문"),
            ("manual", "기타")
        ]
    )

    # 접촉 목적 (초회/리마인드/청약/사후관리 등)
    purpose = models.CharField(
        max_length=30,
        choices=[
            ("initial", "초회"),
            ("followup", "후속"),
            ("proposal", "제안"),
            ("contract", "청약"),
            ("support", "사후관리"),
            ("etc", "기타")
        ],
        default="etc"
    )

    # 자동인지 수동인지 구분
    is_auto = models.BooleanField(default=False)

    # 상세 메모
    memo = models.TextField(blank=True)

    # 접촉 시점
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
