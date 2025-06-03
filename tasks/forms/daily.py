# tasks/forms/daily.py
from django import forms
from activity.models import DailyStandardActivity


class DailyActivityForm(forms.ModelForm):
    class Meta:
        model = DailyStandardActivity
        exclude = ['user', 'date', 'created_at', 'updated_at']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 2}),
        }
