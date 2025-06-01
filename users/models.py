from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('planner', '설계사'),
        ('manager', '지점장'),
        ('branch', '본사관리자'),
    )

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=64, blank=True, null=True)
    user_type = models.CharField(max_length=16, choices=USER_TYPE_CHOICES)
    branch = models.ForeignKey('customers.Branch', on_delete=models.SET_NULL, null=True, blank=True)

    is_subscribed = models.BooleanField(default=False)
    subscription_plan = models.CharField(max_length=16, blank=True, null=True)
    subscription_expires_at = models.DateTimeField(blank=True, null=True)

    last_login = models.DateTimeField(blank=True, null=True)
    login_attempts = models.IntegerField(default=0)

    status = models.CharField(max_length=16, default='active')  # active, suspended 등
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
