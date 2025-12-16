from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import JsonResponse
from notifications import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("notifications.urls")),
    path('health/', views.health_check),
    # redirect root to API
    path("", RedirectView.as_view(url="/api/", permanent=False)),
]

# Customize admin site
admin.site.site_header = "Library Notifications Administration"
admin.site.site_title = "Notifications Admin"
admin.site.index_title = "Welcome to Library Notifications Service"