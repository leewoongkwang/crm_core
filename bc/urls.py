from django.urls import path
from .views import card_view

app_name = 'bc'

urlpatterns = [
    path('<slug:slug>/', card_view, name='detail'),
]
