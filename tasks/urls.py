from django.urls import path
from tasks.views.entry import task_entry_view
from tasks.views.adjust import adjust_kpi_view
from tasks.views.adjust import (
    advance_touch_action_view,
    revert_touch_action_view,
    complete_touch_action_view,
)

app_name = 'tasks'

urlpatterns = [
    path('', task_entry_view, name='entry'),
    path("adjust/", adjust_kpi_view, name="adjust_kpi"),
    path("touchlog/advance/", advance_touch_action_view, name="advance_touch"),
    path("touchlog/revert/", revert_touch_action_view, name="revert_touch"),
    path("touchlog/complete/", complete_touch_action_view, name="complete_touch"),
]
