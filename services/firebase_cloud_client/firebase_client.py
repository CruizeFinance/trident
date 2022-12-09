import firebase_admin
from firebase_admin import credentials, firestore
from services.vault_security.vault_security import VaultSecurity

"""
 class FirebaseClient is responsible for initializing firebase_admin client.
 It have to method create_firebase_client_instance() that initializing firebase_admin client and get_firebase_client
 that return firebase_admin client.
"""


# TODO: make this class singleton
class FirebaseClient(object):
    def __init__(self):
        self.client = None
        self.firebase_credentials = None
        self.vault_security_obj=VaultSecurity()

    def create_firebase_client_instance(self):
        if self.firebase_credentials is None:
            self.firebase_credentials = self.vault_security_obj.fetch('firebase_credentials')
        cred = credentials.Certificate(
            self.firebase_credentials
        )
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()
        return self.client

    @property
    def get_firebase_client(self):
        if self.client is not None:
            return self.client
        print("FirebaseClient :: Firebase client is None")
        return self.create_firebase_client_instance()
