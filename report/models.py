# report/models.py
from django.db import models
from customers.models import Customer
from django.conf import settings

class Report(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_url = models.CharField(max_length=256)  # S3 또는 로컬 경로
    parse_json = models.JSONField(null=True, blank=True)  # 파싱 결과 저장
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.customer.name} ({self.uploaded_at.date()})"