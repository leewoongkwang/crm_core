from django.urls import path
from contracts.views.customer_tab import customer_contract_partial

urlpatterns = [
    path("customer/<int:pk>/partial/", customer_contract_partial, name="contract_tab_customer"),
]
