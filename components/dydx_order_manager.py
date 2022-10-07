import time

from dydx3 import constants
from tests.constants import SEVEN_DAYS_S

from components import FirebaseDataManager, PriceFloorManager
from services import DydxOrder, DydxAdmin

# class: DydxOrderManager - is responsible for managing order on dydx.
from services.contracts.chainlink import ChainlinkPriceFeed
from utilities import cruize_constants
from utilities.enums import AssetCodes


class DydxOrderManager:
    def __init__(self):
        self.dydx_admin = DydxAdmin()
        self.chainlink_price_feed = ChainlinkPriceFeed()

    def create_order(self, order_params):
        dydx_order = DydxOrder()
        firebase_order_manager_obj = FirebaseDataManager()
        # we have to keep separate volume of btc and eth to open different position on dydx.
        # total_btc_volume * 5 --> would be the open size for the btc
        # total_eth_volume * 5 --> would be the open size for eth
        order_information = dydx_order.create_order(order_params)
        dydx_order_details = vars(order_information)
        dydx_order_details = dydx_order_details["data"]["order"]
        firebase_order_manager_obj.store_data(dydx_order_details,dydx_order_details['id'] ,"dydx_orders")
        return order_information

    def calculate_open_close_price(self, asset_pair, open_price):
        bids = 0
        bids_consumed = 0
        price_floor_manager_obj = PriceFloorManager()
        dydx_order_obj = DydxOrder()
        asset_order_book = dydx_order_obj.get_order_book(asset_pair)
        highest_bids = asset_order_book["bids"][0]["size"]
        lowest_asks = asset_order_book["asks"][0]["size"]
        market_price = highest_bids + lowest_asks / 2
        interval = 0
        order_bids = asset_order_book["bids"]
        order_size = open_price / market_price
        while order_size > 0:
            bids += order_bids[interval]["size"]
            bids_consumed += (
                    order_bids[interval]["size"] * order_bids[interval]["price"]
            )
            order_size -= order_bids[interval]["size"]
            interval = +1
        bids_consumed = -((-1 * order_size) * order_bids[interval]["price"])
        obtained_price = bids_consumed / open_price
        slippage = (obtained_price - market_price) / market_price
        # store k value to db

        price_floor = price_floor_manager_obj.get_price_floor(AssetCodes.asset_name.value[asset_pair])
        # P_open close = floor ∗(1 + slippage) ∗(1 + K ∗vol30s)

    """
          :method   - create_order_params: will create order parms for market order on dydx.
          :params   - market_price:current market price of asset.
          :params   - side:side of the asset BUY/SELL.
          :params   - size:size of the position BTC/ETH.
          :params   - market:ETH_USD/BTC_USD.
          :return   - order params 
        """

    def create_order_params(
            self,
            side,
            market,
            size,
            market_price,
    ):
        print(market_price)
        if side == "SELL":
            market_price = int(market_price) + 10
        else:
            market_price = int(market_price) - 10
        dydx_admin = DydxAdmin()
        position_id = dydx_admin.get_position_id()
        order_params = {
            "position_id": position_id,
            "side": side,
            "order_type": constants.ORDER_TYPE_MARKET,
            "market": market,
            "size": size,
            "price": str(market_price),
            "post_only": "false",
            "limit_fee": "0.4",
            "expiration_epoch_seconds": time.time() + SEVEN_DAYS_S + 60,
            "time_in_force": constants.TIME_IN_FORCE_IOC,
        }
        return order_params

    """
      :method   - calculate_asst_volume.
      :params   - market_price:current market price of asset.
      :params   - total_volume:total volume of asset.
      :return   - asset total value in usd.
    """

    def get_asset_price_and_size(self, asset_address,other_asset_volume):
        user = self.dydx_admin.get_account()
        user = vars(user)
        market_price = self.chainlink_price_feed.get_oracle_market_price(asset_address)
        total_volume = user["data"]["account"]["equity"]
        asset_volume = float(total_volume) - float(other_asset_volume)
        asset_volume = float(asset_volume) / market_price
        asset_volume *= cruize_constants.POSITION_LEVERAGE
        asset_volume_with_leverage = str(round(asset_volume, cruize_constants.PRICE_ROUNDED_VALUE))
        asset_details = {'price':market_price,'size':asset_volume_with_leverage}
        return asset_details



