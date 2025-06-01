from django.db import models
from users.models import User


class DailyStandardActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    call_1min = models.IntegerField(default=0)
    call_2min = models.IntegerField(default=0)
    grade_potential = models.IntegerField(default=0)  # 카드가망
    band_verified = models.IntegerField(default=0)

    daily_proposals = models.IntegerField(default=0)
    daily_visit_proposals = models.IntegerField(default=0)

    memo = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"
