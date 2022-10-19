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
    # TODO:  need to deploy the redis server for celery task .
    broker_url="sqs://",
    task_default_queue = "celerybroker",
    task_create_missing_queues = False,
    worker_enable_remote_control = False,
    worker_send_task_events =False,
    broker_transport_options = {
        "predefined_queues": {
            "celerybroker": {
                "url": "https://sqs.us-east-1.amazonaws.com/052637204057/celerybroker",
            },
        },
    }
)
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# all task
# TODO : need to add time interval for each task .
app.conf.beat_schedule = {
    "check_withdrawal": {"task": "check_withdrawal", "schedule": 20.0},
    "open_order_on_dydx": {"task": "open_order_on_dydx", "schedule": 20.0},
    "close_order_on_dydx": {"task": "close_order_on_dydx", "schedule": 20.0},
    "computer_eth_usdc_volatility": {
        "task": "computer_eth_usdc_volatility",
        "schedule": 30.0,
    },
    "computer_btc_usdc_volatility": {
        "task": "computer_btc_usdc_volatility",
        "schedule": 30.0,
    },
    "set_price_floor": {
        "task": "set_price_floor",
        "schedule": 30.0,
    },
}
