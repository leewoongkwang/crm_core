from django.urls import path,include
from customers.views import (  # __init__.py 에서 재정의된 함수들
    customer_list_view,
    customer_add_view,
    customer_edit_view,
    customer_delete_view,
)
from customers.views.detail import CustomerDetailView  # 클래스형 View는 개별 import

app_name = "customers"

urlpatterns = [
    path("list/", customer_list_view, name="customer_list"),
    path("add/", customer_add_view, name="customer_add"),
    path("<int:id>/edit/", customer_edit_view, name="customer_edit"),
    path("<int:id>/delete/", customer_delete_view, name="customer_delete"),


    path("<int:pk>/", CustomerDetailView.as_view(), name="customer_detail"),
    path("touchlog/", include("touchlog.urls")),
]
