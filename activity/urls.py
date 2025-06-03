# activity/urls.py
from django.urls import path
from .views.entry import activity_entry_view
# from .views.summary import activity_summary_view
# from .views.api import activity_api

app_name = 'activity'

urlpatterns = [
    path('', activity_entry_view, name='entry'),
    # path('summary/', activity_summary_view, name='summary'),
    # path('api/data/', activity_api, name='api-data'),
]
