"""Class OrderManager is responsible for storing dydx_orders data in firebase cloud storage.

   It has two method store_on_firebase() that is responsible for storing data in DB.
   Method update_on_firebase() is used to update data in DB. """
from services import DydxAdmin
from services.contracts.chainlink import ChainlinkPriceFeed
from settings_config import firebase_client


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

    def order_params(self):
        order_prams = {"position_id": None, "size": None, "market_price": None}
        chainlink_price_feed_obj = ChainlinkPriceFeed()
        market_price = chainlink_price_feed_obj.get_asset_price(
            "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
        )  # make it dynamic
        admin = DydxAdmin()
        user = admin.get_account()
        user = vars(user)
        user_balance = user["data"]["account"]["equity"]
        position_id = user["data"]["account"]["positionId"]
        size = float(user_balance) / market_price
        size *= 5

        order_prams["size"] = str(round(size, 3))
        order_prams["position_id"] = position_id
        order_prams["market_price"] = market_price
        return order_prams
