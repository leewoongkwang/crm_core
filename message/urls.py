from django.urls import path
from django.shortcuts import render
from message.views.send import send_message_view
from message.views.send import sender_ping_view
from message.views.api import sender_shutdown_view

from message.views.api import lock_and_fetch_messages, report_message_status
from message.views.api import message_status_summary
from message.views.api import launcher_ping, launcher_ping_latest
from customers.models import Customer
app_name = "message"

urlpatterns = [
    path("send/", send_message_view, name="send"),
    path("api/message/lock/", lock_and_fetch_messages, name="api_lock"),
    path("api/message/report/", report_message_status, name="api_report"),
    path("api/status-summary/", message_status_summary, name="message_status_summary"),
    path("sender-ping", sender_ping_view, name="sender-ping"),
    path("launcher-ping", launcher_ping, name="launcher_ping"),
    path("launcher-ping-latest", launcher_ping_latest, name="launcher_ping_latest"),
    path("api/sender-shutdown", sender_shutdown_view, name="sender-shutdown"),
]
