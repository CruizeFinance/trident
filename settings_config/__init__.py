from settings_config import celery_config
from services import DydxPClient
from services.vault_security.vault_security import VaultSecurity
from services.firebase_cloud_client import FirebaseClient
asset_dydx_instance = {}
vault_security_obj = VaultSecurity()
dydx_p_client_obj = DydxPClient()
dydx_credentials = vault_security_obj.fetch("dydx_instances")
sentry_dns = vault_security_obj.fetch("sentry_dns")
project_secret_key = vault_security_obj.fetch('secret_key')


def initialize_dydx_instances():
    for key, value in dydx_credentials.items():
        asset_dydx_instance[key] = {
            "dydx_data": value,
            "dydx_instance": dydx_p_client_obj.create_dydx_instance(value),
        }


def initialize_firebase_client():
    global firebase_client
    firebase_client = None
    firebase_client_obj = FirebaseClient()
    if not firebase_client:
        firebase_client = firebase_client_obj.get_firebase_client
    return firebase_client


initialize_dydx_instances()
firebase_client = initialize_firebase_client()

celery_app = celery_config.app
__all__ = "celery_app"
