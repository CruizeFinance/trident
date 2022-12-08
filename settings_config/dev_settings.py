from django.core.wsgi import get_wsgi_application
from .common import *
from settings_config import project_secret_key
SECRET_KEY = project_secret_key['data']
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "52.72.210.207", "3.210.156.188"]

WSGI_APPLICATION = "settings_config.wsgi.application"

application = get_wsgi_application()
