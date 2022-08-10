from settings_config import firebase_client

"""Class OrderManager is responsible for storing dydx_orders data in firebase cloud storage.
   It has two method store_order_data() that is responsible for storing data in DB.
   Method update_order_data() is used to update data in DB. """


class OrderManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    def store_order_data(self, order_data):
        self.firebase_client.collection("dydx_orders").document(order_data["id"]).set(
            order_data
        )

    def update_order_data(self, order_id):
        self.firebase_client.collection("dydx_orders").document(order_id).update(
            {"status": "CANCEL"}
        )

    def fetch_orders(self, order_id=None):
        db_ref = self.firebase_client.collection("dydx_orders")

        if order_id:
            order = db_ref.document(str(order_id)).get()
            return vars(order).get("_data")

        order_objects = db_ref.get()
        orders = []
        for order in order_objects:
            orders.append(vars(order)["_data"])
        return orders
