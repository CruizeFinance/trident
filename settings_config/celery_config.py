from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_config.production_settings")
app = Celery("trident", include=["services.celery.celery"])
app.conf.enable_utc = True
app.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=True,
    accept_content=["json"],
    result_accept_content=["json"],
    task_always_eager=True,
    task_store_eager_result=True,
    broker_url="sqs://",
    task_default_queue="celerybroker",
    task_create_missing_queues=False,
    worker_enable_remote_control=False,
    worker_send_task_events=False,
    broker_transport_options={
        "predefined_queues": {
            "celerybroker": {
                "url": "https://sqs.us-east-1.amazonaws.com/052637204057/celerybroker",
            },
        },
    },
    # timezone="Asia/Kolkata",
    # enable_utc=True,
    # accept_content=["json"],
    # result_accept_content=["json"],
    # task_always_eager=True,
    # task_store_eager_result=True,
    # broker_url="redis://127.0.0.1:6379/0",
    # result_backend="redis://127.0.0.1:6379/1",
)
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# all task
# TODO : need to add time interval for each task .
app.conf.beat_schedule = {
    "check_withdrawal": {"task": "check_withdrawal", "schedule": 20.0},
    "open_order_on_dydx": {"task": "open_order_on_dydx", "schedule": 40.0},
    "close_order_on_dydx": {"task": "close_order_on_dydx", "schedule": 40.0},
    "compute_eth_usdc_volatility": {
        "task": "compute_eth_usdc_volatility",
        "schedule": 30.0,
    },
    "compute_btc_usdc_volatility": {
        "task": "compute_btc_usdc_volatility",
        "schedule": 30.0,
    },
    "set_price_floor": {
        "task": "set_price_floor",
        "schedule": 30.0,
    },
    "store_asset_apy": {"task": "store_asset_apy", "schedule": 30},
}
