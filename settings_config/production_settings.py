from .common import *
from django.core.wsgi import get_wsgi_application

SECRET_KEY = "j7qelfcc!qe*%((o3p0ju20obkx^j9+9#%%d-t15gqnz^*$om#"
DEBUG = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://test.app.cruize.finance",
    "https://www.test.app.cruize.finance",
]
ALLOWED_HOSTS = ["52.20.55.165","test2.trident.cruize.finance", "test1.trident.cruize.finance","test.trident.cruize.finance","3.210.156.188","3.231.35.12"]

WSGI_APPLICATION = "settings_config.wsgi.application"

application = get_wsgi_application()
