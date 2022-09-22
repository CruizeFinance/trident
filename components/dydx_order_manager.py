import time
from datetime import datetime, timedelta

import pandas
from dateutil.relativedelta import relativedelta
from dydx3 import constants
from tests.constants import SEVEN_DAYS_S
from components import PriceFloorManager
from services import DydxOrder, DydxAdmin
from services.binance_client.binance_client import BinanceClient
from services.contracts.chainlink import ChainlinkPriceFeed
from utilities import cruize_constants
from utilities.enums import AssetCodes


# class: DydxOrderManager - is responsible for managing order on dydx.


class DydxOrderManager:
    def __init__(self):
        self.dydx_admin = DydxAdmin()
        self.chainlink_price_feed = ChainlinkPriceFeed()
        self.binance_client_obj = BinanceClient()
        self.price_floor_manager_obj = PriceFloorManager()

    def create_order(self, order_params):
        dydx_order = DydxOrder()
        # we have to keep separate volume of btc and eth to open different position on dydx.
        # total_btc_volume * 5 --> would be the open size for the btc
        # total_eth_volume * 5 --> would be the open size for eth
        order_information = dydx_order.create_order(order_params)
        dydx_order_details = vars(order_information)
        dydx_order_details = dydx_order_details["data"]["order"]
        return order_information

    def calculate_open_close_price(self, asset_pair, eth_order_size, symbol):
        bids_consumed = 0
        dydx_order_obj = DydxOrder()
        asset_order_book = dydx_order_obj.get_order_book(asset_pair)
        order_asks = asset_order_book["asks"]
        order_bids = asset_order_book["bids"]
        lowest_ask = float(order_asks[0]["price"])
        highest_bid = float(order_bids[0]["price"])
        market_price = (highest_bid + lowest_ask) / 2
        interval = 0
        asset_order_size = eth_order_size
        while asset_order_size > 0:
            bids_consumed += float(
                (
                    float(order_bids[interval]["size"])
                    * float(order_bids[interval]["price"])
                )
            )
            asset_order_size -= float(order_bids[interval]["size"])
            interval += 1

        if asset_order_size <= 0:
            bids_consumed -= abs(
                ((-1 * asset_order_size) * float(order_bids[interval - 1]["price"]))
            )

        obtained_price = bids_consumed / eth_order_size

        slippage = (obtained_price - market_price) / market_price

        price_floor = self.price_floor_manager_obj.get_price_floor(
            AssetCodes.asset_name.value[asset_pair]
        )
        ema_data = self.price_floor_manager_obj.firebase_data_manager_obj.fetch_data("ema_data", symbol)

        ema = ema_data.get("_data")['ema']
        # K must change ,K being variable will cover price movement
        # within 30s under normal market conditions
        K = 2
        p_open_close = (price_floor * (1 + slippage)) * (
            (1 + ema["mu_ema"]) + (K * ema["sigma_ema"])
        )
        return p_open_close

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

    def get_asset_price_and_size(self, asset_address, other_asset_volume):
        user = self.dydx_admin.get_account()
        user = vars(user)
        market_price = self.chainlink_price_feed.get_oracle_market_price(asset_address)
        total_volume = user["data"]["account"]["equity"]
        asset_volume = float(total_volume) - float(other_asset_volume)
        asset_volume = float(asset_volume) / market_price
        asset_volume *= cruize_constants.POSITION_LEVERAGE
        asset_volume_with_leverage = str(
            round(asset_volume, cruize_constants.PRICE_ROUNDED_VALUE)
        )
        asset_details = {"price": market_price, "size": asset_volume_with_leverage}

        return asset_details

    def compute_market_volatility(self, prices_data):
        volatility_data = {"sigma_ema": None, "mu_ema": None}
        percentage_EMA = []
        for i in range(1, len(prices_data)):
            percentage_EMA.append(float(prices_data[i]) / float(prices_data[i - 1]))
        data_frame_ema = pandas.DataFrame(percentage_EMA)
        actual_ema = data_frame_ema.ewm(alpha=0.8, adjust=False)
        sigma_ema = actual_ema.std().mean()
        mu_ema = actual_ema.mean().mean() - 1
        volatility_data["sigma_ema"] = float(sigma_ema)
        volatility_data["mu_ema"] = float(mu_ema)
        return volatility_data

    def market_volatility(self, symbol):
        volatility_data = {}
        # fetch price data from db .
        price_data = self.price_floor_manager_obj.firebase_data_manager_obj.fetch_data(
            "price_data", symbol
        )

        # TODO :  have to change the start time and end time in both if and else condition's

        if price_data is None:

            # if db price data is none than  fetch prices for past 6 months .
            end_time = datetime.utcnow()
            start_time = end_time - relativedelta(weeks=1)
            prices = self.binance_client_obj.price_data_per_interval(
                symbol=symbol,
                start_time=str(start_time.timestamp() * 1000),
                end_time=str(end_time.timestamp() * 1000),
            )
            price_data = prices
            volatility_data = self.compute_market_volatility(prices)
        else:
            end_time = datetime.utcnow()
            start_time = datetime.utcnow() - timedelta(minutes=1)
            prices = self.binance_client_obj.price_data_per_interval(
                symbol=symbol,
                end_time=str(end_time.timestamp() * 1000),
                start_time=str(start_time.timestamp() * 1000),
            )
            price_data = price_data["prices"]
            price_data = price_data.split(",")
            # remove old price from the  list that should be equal to  new price's length  .
            del price_data[0 : len(prices) + 1]
            # append new prices to price_data array
            for i in range(len(prices)):
                price_data.append(prices[i])

            # compute market volatility .
            volatility_data = self.compute_market_volatility(prices_data=price_data)
        price_data = ",".join(price_data)
        self.price_floor_manager_obj.firebase_data_manager_obj.store_data(
            "price_data", symbol, {"prices": price_data}
        )
        self.price_floor_manager_obj.firebase_data_manager_obj.store_data(
            "ema_data", symbol, {"ema": volatility_data}
        )


if __name__ == "__main__":
    a = DydxOrderManager()
    a = a.calculate_open_close_price("BTC-USD", 10, "BTCBUSD")
    print(a)
