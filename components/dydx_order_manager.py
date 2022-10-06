from components import FirebaseDataManager, PriceFloorManager
from services import DydxOrder
from services.dydx_client.dydx_order_book import DydxOrderBook


# class: DydxOrderManager - is responsible for managing order on dydx.
from utilities.enums import AssetName


class DydxOrderManager:
    def create_order(self, order_params):
        dydx_order = DydxOrder()
        firebase_order_manager_obj = FirebaseDataManager()
        # we have to keep separate volume of btc and eth to open different position on dydx.
        # total_btc_volume * 5 --> would be the open size for the btc
        # total_eth_volume * 5 --> would be the open size for eth
        order_information = dydx_order.create_order(order_params)
        dydx_order_details = vars(order_information)
        dydx_order_details = dydx_order_details["data"]["order"]
        firebase_order_manager_obj.store_data(dydx_order_details, "dydx_orders")
        return order_information

    def calculate_open_close_price(self, asset_pair, open_price):
        bids = 0
        bids_consumed = 0
        price_floor_manager_obj = PriceFloorManager()
        dydx_orderbook_obj = DydxOrderBook()
        asset_order_book = dydx_orderbook_obj.get_order_book(asset_pair)
        highest_bids = asset_order_book['bids'][0]['size']
        lowest_asks = asset_order_book['asks'][0]['size']
        market_price = highest_bids + lowest_asks / 2
        interval = 0
        order_bids = asset_order_book['bids']
        order_size = open_price / market_price
        while order_size > 0:
            bids += (order_bids[interval]['size'])
            bids_consumed += (order_bids[interval]['size'] * order_bids[interval]['price'])
            order_size -= order_bids[interval]['size']
            interval = +1
        bids_consumed = - ((-1 * order_size) * order_bids[interval]['price'])
        obtained_price = bids_consumed / open_price
        slippage = (obtained_price - market_price / market_price)
        # store k value to db

        price_floor = price_floor_manager_obj.calculate_price_floor(AssetName.asset_name.value[asset_pair])
        # P_open close = floor ∗(1 + slippage) ∗(1 + K ∗vol30s)
