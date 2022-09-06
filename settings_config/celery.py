from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_config.settings")
app = Celery("trident", include=["services.celery.celery"])
app.conf.enable_utc = True
app.conf.update(timezone="Asia/Kolkata", enable_utc=True, accept_content=['json'], result_accept_content=['json'],
                task_always_eager=True, task_store_eager_result=True, broker_url="redis://127.0.0.1:6379/0",
                result_backend="redis://127.0.0.1:6379/1")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)