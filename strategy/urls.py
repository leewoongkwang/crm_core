from django.urls import path
from .views.entry import strategy_entry_view

app_name = 'strategy'

urlpatterns = [
    path('', strategy_entry_view, name='entry'),
]
