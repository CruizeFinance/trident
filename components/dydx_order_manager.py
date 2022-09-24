import time
from tests.constants import SEVEN_DAYS_S
from components import FirebaseDataManager
from services import DydxOrder, DydxAdmin
from utilities import cruize_constants

# class: DydxOrderManager - is responsible for managing order on dydx.
class DydxOrderManager:
    def create_order(self, order_params):
        dydx_order = DydxOrder()
        dydx_admin = DydxAdmin()
        firebase_order_manager_obj = FirebaseDataManager()
        position_id = dydx_admin.get_position_id()
        market_price = order_params["market_price"]
        # we have to keep separate volume of btc and eth to open different position on dydx.
        # total_btc_volume * 5 --> would be the open size for the btc
        # total_eth_valume * 5 --> would be the open size for eth
        print(order_params["size"])
        order_information = dydx_order.create_order(
            {
                "position_id": position_id,
                "market": order_params["market"],
                "side": order_params["side"],
                "order_type": "MARKET",
                "post_only": "false",
                "size": order_params["size"],
                "price": str(market_price),
                "limit_fee": "0.4",
                "expiration_epoch_seconds": time.time() + SEVEN_DAYS_S + 60,
                "time_in_force": cruize_constants.TIME_IN_FORCE_IOC,
            }
        )
        dydx_order_details = vars(order_information)
        dydx_order_details = dydx_order_details["data"]["order"]
        firebase_order_manager_obj.store_data(dydx_order_details, "dydx_orders")
        return order_information
