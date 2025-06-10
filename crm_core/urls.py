from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("home/", include("home.urls")),
    path("customer/", include("customers.urls")),
    path('strategy/', include('strategy.urls')),
    path("touchlog/", include("touchlog.urls")),
    path("analysis/", include("analysis.urls")),
    path("report/", include("report.urls")),
    path("contracts/", include("contracts.urls")),
    path('activity/', include('activity.urls')),
    path('tasks/', include('tasks.urls')),
    path("message/", include("message.urls")),

]
