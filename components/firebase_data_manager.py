import datetime
import time

from settings_config import firebase_client


class FirebaseDataManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    def update_data(self, order_id, collection, status):
        self.firebase_client.collection(collection).document(order_id).update(
            {"status": status}
        )

    def store_data(self, data, collection_name):
        user_address = data.get("user_address", "Not found")
        if user_address == "Not found":
            self.firebase_client.collection(collection_name).document(data["id"]).set(
                data
            )
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

    def fetch_transaction_data(self, collection, data):
        transaction_data = (
            self.firebase_client.collection(collection)
            .document(data["user_address"])
            .collection("transactions")
            .get()
        )

        if transaction_data  == []:
            return f"address {data['user_address']} don't have any transaction."
        data = []
        if transaction_data is not None:
            for tnx_data in transaction_data:
                data.append(tnx_data.to_dict())
        return data


if __name__ == "__main__":
    pass
    a = FirebaseDataManager()
    # a = a.store_data({"user_address": "x0", "asset": "ETH", "tnx_hash": "0x1"},"user_tnx")
    a = a.fetch_transaction_data(
        "user_tnx", {"user_address": "x0", "asset": "ETH", "tnx_hash": "0x143"}
    )
