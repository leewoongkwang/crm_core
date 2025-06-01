# customers/models.py

from django.db import models
from users.models import User


class Customer(models.Model):
    ATTRIBUTE_CHOICES = (
        ('인콜', '인콜'),
        ('카드', '카드'),
        ('멤버스', '멤버스'),
        ('소개', '소개'),
        ('지인', '지인'),
        ('가족', '가족'),
    )
    GRADE_CHOICES = (
        ('충성', '충성'),
        ('가망', '가망'),
        ('유령', '유령'),
        ('미가망', '미가망'),
    )
    PROPENSITY_CHOICES = (
        ('니즈확실', '니즈확실'),
        ('정보위주', '정보위주'),
        ('친밀위주', '친밀위주'),
    )
    INTIMACY_CHOICES = (
        ('친함', '친함'),
        ('중립', '중립'),
        ('경계', '경계'),
    )
    PRIORITY_CHOICES = (
        ('상', '상'),
        ('중', '중'),
        ('하', '하'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    phone_encrypted = models.CharField(max_length=64)
    birth_encrypted = models.CharField(max_length=64)
    gender = models.CharField(max_length=1)

    attribute = models.CharField(max_length=16, choices=ATTRIBUTE_CHOICES, blank=True)
    grade = models.CharField(max_length=16, choices=GRADE_CHOICES, blank=True)
    propensity = models.CharField(max_length=16, choices=PROPENSITY_CHOICES, blank=True)
    intimacy = models.CharField(max_length=16, choices=INTIMACY_CHOICES, blank=True)
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, blank=True)

    is_target_customer = models.BooleanField(default=False)
    is_active_touching = models.BooleanField(default=False)

    sent_business_card = models.BooleanField(default=False)
    sent_report = models.BooleanField(default=False)
    sent_pre_call_sms = models.BooleanField(default=False)
    first_call_done = models.BooleanField(default=False)
    sent_proposal_on_reject = models.BooleanField(default=False)
    second_call_done = models.BooleanField(default=False)
    suggested_visit = models.BooleanField(default=False)

    memo = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=64)
    region = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
