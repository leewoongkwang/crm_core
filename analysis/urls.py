from django.urls import path
from analysis.views.detail import analysis_detail_view

app_name = "analysis"

urlpatterns = [
    path('<int:report_id>/', analysis_detail_view, name='analysis_detail'),
]
