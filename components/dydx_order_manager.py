import time
from tests.constants import SEVEN_DAYS_S
from components import FirebaseDataManager
from services import DydxOrder, DydxAdmin
from utilities import cruize_constants

# class: DydxOrderManager - is responsible for managing order on dydx.
class DydxOrderManager:
    def create_order(self, order_params):
        dydx_order = DydxOrder()
        firebase_order_manager_obj = FirebaseDataManager()
        # we have to keep separate volume of btc and eth to open different position on dydx.
        # total_btc_volume * 5 --> would be the open size for the btc
        # total_eth_valume * 5 --> would be the open size for eth
        order_information = dydx_order.create_order(order_params)
        dydx_order_details = vars(order_information)
        dydx_order_details = dydx_order_details["data"]["order"]
        firebase_order_manager_obj.store_data(dydx_order_details, "dydx_orders")
        return order_information
