from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Strategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    monthly_cpc_goal = models.IntegerField(default=0)
    weekly_cpc_goal = models.IntegerField(default=0)
    daily_call_1min = models.IntegerField(default=0)
    daily_call_2min = models.IntegerField(default=0)
    weekly_call_1min = models.IntegerField(default=0)
    weekly_call_2min = models.IntegerField(default=0)
    daily_proposals = models.IntegerField(default=0)
    daily_visit_proposals = models.IntegerField(default=0)
    daily_grade_potential = models.IntegerField(default=0)
    daily_band_verified = models.IntegerField(default=0)
    memo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'year', 'month')

    def __str__(self):
        return f'{self.user.username} - {self.year}.{self.month}'
