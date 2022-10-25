from .common import *
from django.core.wsgi import get_wsgi_application

SECRET_KEY = "j7qelfcc!qe*%((o3p0ju20obkx^j9+9#%%d-t15gqnz^*$om#"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1"]

WSGI_APPLICATION = "settings_config.wsgi.application"

application = get_wsgi_application()
