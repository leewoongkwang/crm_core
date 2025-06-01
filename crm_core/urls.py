from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("home/", include("home.urls")),
    path("customer/", include("customers.urls")),
    path('strategy/', include('strategy.urls')),
    path("touch/", include("touchlog.urls")),
    path("analysis/", include("reports.urls")),

]
