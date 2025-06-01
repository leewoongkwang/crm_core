from django.db import models
from customers.models import Customer


class Contract(models.Model):
    STATUS_CHOICES = (
        ('청약', '청약'),
        ('유지', '유지'),
        ('만기', '만기'),
        ('해지', '해지'),
        ('기타', '기타'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)  # 보험상품명
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='청약')
    signed_at = models.DateTimeField()
    expired_at = models.DateTimeField(blank=True, null=True)
    premium = models.IntegerField()  # 월납/연납 보험료

    def __str__(self):
        return f"{self.customer.name} - {self.name} ({self.status})"
