import time

# TODO : refactor this file .
from services.firebase_cloud_client import FirebaseClient
from settings_config import firebase_client


class FirebaseDataManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    def get_firebase_client(self):
        if self.firebase_client is None:
            self.firebase_client = FirebaseClient().get_firebase_client
        return self.firebase_client

    def update_data(self, order_id, collection, data):
        self.firebase_client = self.get_firebase_client()
        self.firebase_client.collection(collection).document(order_id).update(data)

    def store_data(self, data, id, collection_name):
        self.firebase_client = self.get_firebase_client()
        self.firebase_client.collection(collection_name).document(id).set(data)

    def bulk_store(self, data, collection_name, field):
        self.firebase_client = self.get_firebase_client()
        batch = self.firebase_client.batch()
        for key, value in data.items():
            write = self.firebase_client.collection(collection_name).document(key)
            batch.set(write, {field: str(value)})
        batch.commit()

    def store_sub_collections(
        self, data, collection, document_name, sub_collection, sub_document
    ):
        self.firebase_client = self.get_firebase_client()
        data["timestamp"] = time.time()
        self.firebase_client.collection(collection).document(document_name).collection(
            sub_collection
        ).document(sub_document).set(data)

    def fetch_sub_collections(self, collection, document_name, sub_collection):
        self.firebase_client = self.get_firebase_client()
        firebase_data = (
            self.firebase_client.collection(collection)
            .document(document_name)
            .collection(sub_collection)
            .get()
        )
        return firebase_data

    def fetch_data(self, collection_name, document_name):
        self.firebase_client = self.get_firebase_client()
        firebase_data = (
            self.firebase_client.collection(collection_name)
            .document(document_name)
            .get()
        )
        if firebase_data is not None:
            firebase_data = vars(firebase_data)
        return firebase_data.get("_data", None)

    def fetch_collections(self, collection_name):
        self.firebase_client = self.get_firebase_client()
        collection_obj = self.firebase_client.collection(collection_name)
        collection_data = collection_obj.stream()
        return collection_data


if __name__ == "__main__":
    a = FirebaseDataManager()
    # a = a.store_data({"user_address": "x0", "asset": "ETH", "tnx_hash": "0x1"},"user_tnx")
    # print(a.fetch_collections())
