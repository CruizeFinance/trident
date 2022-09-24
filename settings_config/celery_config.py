from __future__ import absolute_import, unicode_literals
import os


from celery import Celery
from django.conf import settings

from utilities import cruize_constants

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_config.settings")
app = Celery("trident", include=["services.celery.celery"])
app.conf.enable_utc = True
app.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=True,
    accept_content=["json"],
    result_accept_content=["json"],
    task_always_eager=True,
    task_store_eager_result=True,
    broker_url=cruize_constants.BROKER_URL,
    result_backend=cruize_constants.RESULT_BACKEND,
)
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# all task
app.conf.beat_schedule = {
    # "check_withdrawal": {"task": "check_withdrawal", "schedule": 20.0},
    "open_order_on_dydx": {"task": "open_order_on_dydx", "schedule": 20.0},
    # "close_order_on_dydx": {"task": "close_order_on_dydx", "schedule": 20.0},
}
