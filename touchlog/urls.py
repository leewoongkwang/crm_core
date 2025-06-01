from django.urls import path
from .views import touch_view

app_name = "touchlog"

urlpatterns = [
    path("", touch_view, name="touch"),
]
