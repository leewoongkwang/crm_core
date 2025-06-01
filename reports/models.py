from django.db import models
from customers.models import Customer
from django.contrib.auth import get_user_model
User = get_user_model()


class Report(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file_url = models.CharField(max_length=256)  # S3 or 경로 문자열
    parse_json = models.TextField(blank=True)    # 원본 JSON 저장

    uploaded_at = models.DateTimeField(auto_now_add=True)

    # 선택 보장 항목 상태들 (optional - 기준 JSON 기반)
    diagnosis_status = models.CharField(max_length=8, blank=True, null=True)
    surgery_status = models.CharField(max_length=8, blank=True, null=True)
    traffic_support_status = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return f"Report for {self.customer.name} - {self.uploaded_at.strftime('%Y-%m-%d')}"
