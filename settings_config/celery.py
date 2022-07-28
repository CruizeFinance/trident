from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_config.settings")
app = Celery("trident")
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")
app.config_from_object(settings, namespace="CELERY")


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
