# customers/models.py

from django.db import models
from django.contrib.auth import get_user_model
from utils.age import calculate_insurance_age
from utils.age import calculate_insurance_birthday
from datetime import date
User = get_user_model()

class Customer(models.Model):
    ATTRIBUTE_CHOICES = (
        ('인콜', '인콜'),
        ('카드', '카드'),
        ('멤버스', '멤버스'),
        ('소개', '소개'),
        ('지인', '지인'),
        ('가족', '가족'),
    )
    GENDER_CHOICES = (
    ("M", "남성"),
    ("F", "여성"),
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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    attribute = models.CharField(max_length=16, choices=ATTRIBUTE_CHOICES, blank=True)
    grade = models.CharField(max_length=16, choices=GRADE_CHOICES, blank=True)
    propensity = models.CharField(max_length=16, choices=PROPENSITY_CHOICES, blank=True)
    intimacy = models.CharField(max_length=16, choices=INTIMACY_CHOICES, blank=True)
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, blank=True)

    is_target_customer = models.BooleanField(default=False)
    is_active_touching = models.BooleanField(default=False)

    TOUCH_STEP_CHOICES = [
        ("report", "리포트 발송"),
        ("pre_sms", "콜 전 문자"),
        ("call1", "1차 콜"),
        ("reject_sms", "거절 후 제안"),
        ("call2", "2차 콜"),
        ("visit", "방문 제안"),
        ("done", "완료"),
    ]
    current_touch_step = models.CharField(
        max_length=20,
        choices=TOUCH_STEP_CHOICES,
        default="report",
        help_text="현재 고객의 접촉 단계"
    )

    memo = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def insurance_age(self):
        try:
            if not self.birth_encrypted or len(self.birth_encrypted) != 8:
                return None
            birth = self.birth_encrypted  # e.g. 19910802
            birth_date_str = f"{birth[:4]}-{birth[4:6]}-{birth[6:]}"
            today_str = date.today().isoformat()
            age = calculate_insurance_age(birth_date_str, today_str)
            return age
        except Exception as e:
            return None

    @property
    def insurance_birthday(self):
        if not self.birth_encrypted:
            return None
        try:
            birth = self.birth_encrypted
            birth_date_str = f"{birth[:4]}-{birth[4:6]}-{birth[6:]}"
            return calculate_insurance_birthday(birth_date_str)
        except:
            return 
            
    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=64)
    region = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
