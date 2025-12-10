from __future__ import annotations
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_notifications_service.settings")

# Create Celery application
app = Celery("library_notifications_service")

# Load configuration from Django settings with CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks from all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')