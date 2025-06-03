from django.urls import path
from tasks.views.entry import task_entry_view

app_name = 'tasks'

urlpatterns = [
    path('', task_entry_view, name='entry'),
]
