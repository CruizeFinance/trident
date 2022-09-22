import time

from services.firebase_cloud_client import FirebaseClient


# TODO : refactor this file .
class FirebaseDataManager(object):
    def __init__(self):
        self.firebase_client = FirebaseClient()

    def get_firebase_client(self):
        return  self.firebase_client.get_firebase_instance

    def update_data(self, order_id, collection, status):
        firebase_client = self.get_firebase_client()
        firebase_client.collection(collection).document(order_id).update(
            {"status": status}
        )

    def store_data(self, data, id, collection_name):
        firebase_client = self.get_firebase_client()
        firebase_client.collection(collection_name).document(id).set(data)

    def store_sub_collections(self, data, collection, document_name, sub_collection, sub_document):
        firebase_client = self.get_firebase_client()
        data["timestamp"] = time.time()
        firebase_client.collection(collection).document(
            document_name
        ).collection(sub_collection).document(sub_document).set(data)

    def fetch_sub_collections(self, collection, document_name, sub_collection):
        firebase_client = self.get_firebase_client()
        firebase_data = (
            firebase_client.collection(collection).document(
                document_name
            ).collection(sub_collection).get()
        )
        if not firebase_data:
            return f"No data found.."
        data = []
        if data is not None:
            for tnx_data in firebase_data:
                data.append(tnx_data.to_dict())
        return data

    def fetch_data(self, collection_name, document_name):
        firebase_client = self.get_firebase_client()
        data = firebase_client.collection(collection_name).document(document_name).get()
        if data is not None:
            data = vars(data)
        return data

    def fetch_collections(self):
        firebase_client = self.get_firebase_client()
        price_floor_db_obj = firebase_client.collection("price_floor_data")
        price_floor_data = price_floor_db_obj.stream()
        price_floors = {}
        for doc in price_floor_data:
            doc = doc.to_dict()
            price_floors[doc["id"]] = doc["price_floor"]
        return price_floors


if __name__ == "__main__":
    a = FirebaseDataManager()
    # a = a.store_data({"user_address": "x0", "asset": "ETH", "tnx_hash": "0x1"},"user_tnx")
    print(a.fetch_collections())
