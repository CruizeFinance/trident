from services import FirebaseClient


def set_firebase_client():
    firebase_client_obj = FirebaseClient()
    firebase_client = firebase_client_obj.create_firebase_client_instance()
    return firebase_client


firebase_client = set_firebase_client()
from .celery import app as celery_app

__all__ = "celery_app"
