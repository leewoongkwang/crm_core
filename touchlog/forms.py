# /forms.py
from django import forms
from .models import TouchLog

class TouchLogForm(forms.ModelForm):
    class Meta:
        model = TouchLog
        fields = ['customer', 'method', 'memo']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 3}),
        }
