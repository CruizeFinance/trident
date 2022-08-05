from settings_config import firebase_client

"""Class OrderManager is responsible for storing dydx_orders data in firebase cloud storage.
   It has two method store_order_data() that is responsible for storing data in DB.
   Method update_order_data() is used to update data in DB. """


class OrderManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    def store_order_data(self, order_data):
        self.firebase_client.collection('dydx_orders').document(order_data["id"]).set(
            order_data
        )

    def update_order_data(self, order_id):
        self.firebase_client.collection('dydx_orders').document(order_id).update(
            {"status": "Cancel"}
        )
