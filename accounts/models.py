from django.contrib.auth.models import AbstractUser
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=64)
    region = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('planner', '설계사'),
        ('manager', '관리자'),
        ('branch', '운영자'),
    )

    email = models.EmailField(max_length=64, unique=True)
    user_type = models.CharField(max_length=16, choices=USER_TYPE_CHOICES, default='planner')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    subscription_plan = models.CharField(max_length=16, blank=True, null=True)
    subscription_expires_at = models.DateTimeField(blank=True, null=True)
    login_attempts = models.IntegerField(default=0)
    status = models.CharField(max_length=16, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
