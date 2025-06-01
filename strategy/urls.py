from django.urls import path
from .views import strategy_view

app_name = 'strategy'

urlpatterns = [
    path('', strategy_view, name='view'),
]
