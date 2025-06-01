from django.urls import path
from .views import (
    home_view,
    tasks_view,
    customer_list_view,
    customer_detail_view,
    customer_add_view,
    customer_edit_view,
    customer_delete_view,
    strategy_view,
    touch_view,
    analysis_view,
)


urlpatterns = [
    # 홈
    path("home/", home_view, name="home"),
    path("tasks/", tasks_view, name="tasks"),

    # 고객 관련
    path("customer/list/", customer_list_view, name="customer_list"),
    path("customer/add/", customer_add_view, name="customer_add"),
    path("customer/<int:id>/", customer_detail_view, name="customer_detail"),
    path("customer/<int:id>/edit/", customer_edit_view, name="customer_edit"),
    path("customer/<int:id>/delete/", customer_delete_view, name="customer_delete"),

    # 기타 기능
    path("strategy/", strategy_view, name="strategy"),
    path("touch/", touch_view, name="touch"),
    path("analysis/<int:report_id>/", analysis_view, name="analysis_detail"),
]

