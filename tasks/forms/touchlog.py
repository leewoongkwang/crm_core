# tasks/forms/touch.py
from django import forms
from touchlog.models import TouchLog


class TouchLogForm(forms.ModelForm):
    class Meta:
        model = TouchLog
        fields = ['customer', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
