import time
from dydx3 import constants
from tests.constants import SEVEN_DAYS_S
from services import DydxAdmin
from services.contracts.chainlink import ChainlinkPriceFeed
from utilities import cruize_constants
from utilities.datetime_utilities import convert_epoch_to_utcdatetime


class Utilities:
    def __init__(self):
        self.dydx_admin = DydxAdmin()
        self.chainlink_price_feed_obj = ChainlinkPriceFeed()

    """
      :method - get_oracle_market_price.
      :params   - asset_oracle_address:oracle address of asset.
      :return   - asset market price. 
    """

    def get_oracle_market_price(self, asset_oracle_address):
        market_price = self.chainlink_price_feed_obj.get_asset_price(
            asset_oracle_address
        )
        return market_price

    """
      :method - get_asset_volume.
      :params   - market_price:current market price of asset.
      :params   - other_asset_volume:such as BTC volume.
      :return   - asset total value in usd.
    """

    def get_asset_volume(self, other_asset_volume, market_price):
        user = self.dydx_admin.get_account()
        user = vars(user)

        total_volume = user["data"]["account"]["equity"]
        asset_volume = self.calculate_asst_volume(
            total_volume, other_asset_volume, market_price
        )
        return asset_volume

    """
      :method   - calculate_asst_volume.
      :params   - market_price:current market price of asset.
      :params   - total_volume:total volume of asset.
      :return   - asset total value in usd.
    """

    @staticmethod
    def calculate_asst_volume(total_volume, other_asset_volume, market_price):
        asset_volume = float(total_volume) - float(other_asset_volume)
        asset_volume = float(asset_volume) / market_price
        asset_volume *= cruize_constants.POSITION_LEVERAGE
        asset_volume = str(round(asset_volume, cruize_constants.PRICE_ROUNDED_VALUE))
        return asset_volume

    """
        :method   - print_orders_status.
        :params   - market_price:current market price of asset.
        :params   - asset_name:name of the asset BTC/ETH.
        :params   - trigger_price:trigger_price of the asset BTC/ETH.
        :params   - status:status of the asset  position on Dydx.
      """

    def print_orders_status(self, asset_name, market_price, trigger_price, status):
        if trigger_price < market_price:
            print(f" short Position  is already {status}")
        else:
            if market_price < trigger_price:
                price_status = "less than"
            else:
                price_status = "grater than"
            print(
                f"{asset_name} market price {market_price} {price_status} {asset_name} {trigger_price}"
            )

    """
           :method   - print_status_for_order.
           :params   - market_price:current market price of asset.
           :params   - status:status of the asset  position on Dydx.
         """

    def print_status_for_order(self, asset_name, status):
        print(f"{asset_name} short Position  is  {status}")

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
        :method   - get_price_and_size: return size and price of the asset.
        :params   - asset_address:address of asset.
        :params   - other_asset_volume:that is volume of other ERC20 token vs USD.
        :return   - data.
      """

    def get_price_and_size(self, asset_address, other_asset_volume):
        data = {
            "market_price": self.get_oracle_market_price(asset_address),
            "size": None,
        }
        data["size"] = self.get_asset_volume(other_asset_volume, data["market_price"])
        return data



    def formate_price_data(self, price_data):
        for key, value in price_data.items():
            for i, data in enumerate(price_data[key]):
                price_data[key][i][0] = convert_epoch_to_utcdatetime(
                    int(price_data[key][i][0]) / 1000, parser="%m-%d/%H:%M"
                )
                price_data[key][i][1] = round(int(price_data[key][i][1]), 3)

        return price_data



