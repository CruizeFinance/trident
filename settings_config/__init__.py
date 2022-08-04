from services import FirebaseClient


def set_firebase_client():
    print('Order app running')
    firebase_client_obj = FirebaseClient()
    firebase_client = firebase_client_obj.create_firebase_client_instance()
    print('firebase_client: ', firebase_client)
    return firebase_client


firebase_client = set_firebase_client()
