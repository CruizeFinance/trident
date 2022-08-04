import firebase_admin
from firebase_admin import credentials, firestore
import os


# TODO: make this class singleton
class FirebaseClient(object):
    def __init__(self):
        self.client = None

    def create_firebase_client_instance(self):
        cred = credentials.Certificate(
            os.path.abspath(os.path.dirname(__file__)) + "/firebase_config.json"
        )
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()
        return self.client

    @property
    def get_firebase_instance(self):
        if self.client is not None:
            return self.client

        return self.create_firebase_client_instance()