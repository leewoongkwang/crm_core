from django.urls import path
from .views import (
    customer_list_view,
    customer_detail_view,
    customer_add_view,
    customer_edit_view,
    customer_delete_view,
)

app_name = "customers"

urlpatterns = [
    path("list/", customer_list_view, name="customer_list"),
    path("add/", customer_add_view, name="customer_add"),
    path("<int:id>/", customer_detail_view, name="customer_detail"),
    path("<int:id>/edit/", customer_edit_view, name="customer_edit"),
    path("<int:id>/delete/", customer_delete_view, name="customer_delete"),
]
