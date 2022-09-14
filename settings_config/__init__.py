from services import FirebaseClient
from utilities.enums import ContractException


def set_firebase_client():
    firebase_client_obj = FirebaseClient()
    firebase_client = firebase_client_obj.create_firebase_client_instance()
    return firebase_client


def set_error_exceptions():
    exceptions = ContractException()
    return exceptions


contract_exceptions = set_error_exceptions()

firebase_client = set_firebase_client()
from .celery_config import app as celery_app

__all__ = "celery_app"
