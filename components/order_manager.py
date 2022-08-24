from settings_config import firebase_client

"""Class OrderManager is responsible for storing dydx_orders data in firebase cloud storage.

   It has two method store_on_firebase() that is responsible for storing data in DB.
   Method update_on_firebase() is used to update data in DB. """


class OrderManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    def update_data(self, order_id, collection, status):
        self.firebase_client.collection(collection).document(order_id).update(
            {"status": status}
        )

    def store_data(self, data, collection):
        self.firebase_client.collection(collection).document(data["id"]).set(data)

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
