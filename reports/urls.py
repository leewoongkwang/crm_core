# reports/urls.py
from django.urls import path
from reports.views.views import report_upload_view

urlpatterns = [
    path('upload/', report_upload_view, name='report_upload'),
]
