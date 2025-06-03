from django.shortcuts import render

# Create your views here.
# activity/forms.py
from django import forms
from .models import DailyStandardActivity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = DailyStandardActivity
        exclude = ['user', 'date', 'created_at', 'updated_at']
