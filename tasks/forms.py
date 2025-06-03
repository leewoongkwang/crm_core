from django import forms
from activity.models import DailyStandardActivity
from touchlog.models import TouchLog

class KPIForm(forms.ModelForm):
    class Meta:
        model = DailyStandardActivity
        exclude = ['user', 'date', 'created_at']
        widgets = {
            'daily_call_1min': forms.NumberInput(attrs={'min': 0}),
            'daily_call_2min': forms.NumberInput(attrs={'min': 0}),
            'daily_proposals': forms.NumberInput(attrs={'min': 0}),
            'daily_visit_proposals': forms.NumberInput(attrs={'min': 0}),
            'daily_grade_potential': forms.NumberInput(attrs={'min': 0}),
            'daily_band_verified': forms.NumberInput(attrs={'min': 0}),
        }

class TouchForm(forms.ModelForm):
    class Meta:
        model = TouchLog
        exclude = ['user', 'created_at']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 2}),
        }
