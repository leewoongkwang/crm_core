from django.urls import path
from reports.views.customer_tab import customer_report_partial

app_name = "reports"

urlpatterns = [
    path("customer/<int:pk>/partial/", customer_report_partial, name="report_tab_customer"),
]
