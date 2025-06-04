from django import forms
from activity.models import DailyStandardActivity
from touchlog.models import TouchLog

class TouchForm(forms.ModelForm):
    class Meta:
        model = TouchLog
        exclude = ['user', 'created_at']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 2}),
        }
