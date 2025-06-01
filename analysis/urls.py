from django.urls import path
from .views import analysis_view

urlpatterns = [
    path("<int:report_id>/", analysis_view, name="analysis_detail"),
]
