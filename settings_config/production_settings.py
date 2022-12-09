import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from . import sentry_dns, project_secret_key
from django.core.wsgi import get_wsgi_application
from .common import *
SECRET_KEY = project_secret_key['data']
DEBUG = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://test.app.cruize.finance",
    "https://www.test.app.cruize.finance",
    "https://www.beta.app.cruize.finance",
]
ALLOWED_HOSTS = [
    "52.20.55.165",
    "test2.trident.cruize.finance",
    "test1.trident.cruize.finance",
    "test.trident.cruize.finance",
    "trident.test.cruize.finance",
    "3.210.156.188",
    "3.231.35.12",
    "34.225.2.31",
    "beta.trident.cruize.finance",
]

WSGI_APPLICATION = "settings_config.wsgi.application"

application = get_wsgi_application()

# SENTRY SETTINGS

sentry_sdk.init(
    dsn=sentry_dns['dns'],
    integrations=[
        DjangoIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
