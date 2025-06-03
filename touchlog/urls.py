from django.urls import path
from touchlog.views.customer_tab import customer_touchlog_partial

app_name = "touchlog"

urlpatterns = [
    path("customer/<int:pk>/partial/", customer_touchlog_partial, name="touchlog_tab_customer"),
]
