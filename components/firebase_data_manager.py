import time

from services.firebase_cloud_client import FirebaseClient

# TODO : refactor this file .
class FirebaseDataManager(object):
    def __init__(self):
        self.firebase_client = FirebaseClient()
        self.firebase_client = self.firebase_client.get_firebase_instance

    def update_data(self, order_id, collection, status):
        self.firebase_client.collection(collection).document(order_id).update(
            {"status": status}
        )

    def store_data(self, data, id, collection_name):
        user_address = data.get("user_address", "Not found")
        if user_address == "Not found":
            self.firebase_client.collection(collection_name).document(id).set(data)
        else:
            data["timestamp"] = time.time()
            self.firebase_client.collection(collection_name).document(
                data["user_address"]
            ).collection("transactions").document(data["transaction_hash"]).set(data)

    def fetch_orders(self, order_id=None):
        db_ref = self.firebase_client.collection("dydx_orders")
        if order_id:
            order = db_ref.document(str(order_id)).get()
            data = vars(order).get("_data")
            return data
        order_objects = db_ref.get()
        orders = []
        for order in order_objects:
            orders.append(vars(order)["_data"])
        return orders

    def fetch_user_transaction(self, collection, data):
        transaction_data = (
            self.firebase_client.collection(collection)
            .document(data["user_address"])
            .collection("transactions")
            .get()
        )

        if not transaction_data:
            return f"address {data['user_address']} does not have any transaction yet."
        data = []
        if transaction_data is not None:
            for tnx_data in transaction_data:
                data.append(tnx_data.to_dict())
        return data

    def fetch_data(self, document_name, collection_name):
        return (
            self.firebase_client.collection(collection_name)
            .document(document_name)
            .get()
        )

    def store_ema_data(self, collection_name, id, data):
        return self.firebase_client.collection(collection_name).document(id).set(data)

    def get_ema_data(self, collection_name, id):
        price_data = self.firebase_client.collection(collection_name).document(id).get()
        price_data = price_data.to_dict()
        return price_data

    def get_price_floors(self):
        price_floor_db_obj = self.firebase_client.collection("price_floor_data")
        price_floor_data = price_floor_db_obj.stream()
        price_floors = {}
        for doc in price_floor_data:
            doc = doc.to_dict()
            price_floors[doc["id"]] = doc['price_floor']
        return price_floors


if __name__ == "__main__":
    a = FirebaseDataManager()
    # a = a.store_data({"user_address": "x0", "asset": "ETH", "tnx_hash": "0x1"},"user_tnx")
    print(a.get_price_floors())
