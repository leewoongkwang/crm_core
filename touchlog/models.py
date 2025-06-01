from django.db import models
from users.models import User
from customers.models import Customer


class TouchLog(models.Model):
    TYPE_CHOICES = (
        ('14touch', '14터치'),
        ('콜', '콜'),
        ('방문', '방문'),
        ('파싱', '파싱'),
        ('기타', '기타'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    content = models.TextField()
    strategy_note = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    underwriting_status = models.CharField(max_length=16, blank=True)  # Y/N/보류 등
    underwriting_result = models.TextField(blank=True)
    insurance_products = models.TextField(blank=True)

    touched_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.type} - {self.touched_at.strftime('%Y-%m-%d')}"
