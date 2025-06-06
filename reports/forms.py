# reports/forms.py
from django import forms
from .models import Report

class ReportUploadForm(forms.ModelForm):
    pdf_file = forms.FileField(label="PDF 리포트 업로드")

    class Meta:
        model = Report
        fields = ['customer', 'pdf_file']
