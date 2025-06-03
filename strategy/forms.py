from django import forms
from .models import Strategy
from datetime import date

class StrategyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Strategy
        exclude = [
            'user', 'created_at', 'updated_at',
            'year', 'month'
        ]
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        today = date.today()
        if Strategy.objects.filter(
            user=self.user, year=today.year, month=today.month
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("이미 이번 달 전략이 존재합니다.")
        return cleaned_data
