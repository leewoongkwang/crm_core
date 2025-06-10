# report/urls.py
from django.urls import path
from report.views.views import report_upload_view

urlpatterns = [
    path('upload/', report_upload_view, name='report_upload'),
]