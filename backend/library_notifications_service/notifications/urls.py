from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.create_notification, name='create-notification'),
    path('notifications/send_from_template/', views.send_from_template, name='send-from-template'),
    path('notifications/user_notifications/', views.user_notifications, name='user-notifications'),
    path('notifications/stats/', views.stats, name='notification-stats'),
]