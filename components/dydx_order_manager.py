import time
from datetime import datetime, timedelta
import pandas
from dateutil.relativedelta import relativedelta
from dydx3 import constants
from tests.constants import SEVEN_DAYS_S
from components import PriceFloorManager, FirebaseDataManager
from components.transaction_manager import TransactionManager
from services import DydxOrder, DydxAdmin
from services.binance_client.binance_client import BinanceClient
from services.contracts.chainlink import ChainlinkPriceFeed
from settings_config import asset_dydx_instance
from utilities import cruize_constants
from utilities.enums import AssetCodes


"""class::DydxOrderManager is responsible for managing operation on Dydx 
  such us opening and closing  order on dydx, calculating open and close price for position,
  computing market volatility for an asset etc, to perform all of these task there are function written is  the class 
 """


class DydxOrderManager:
    def __init__(self, dydx_client=None):
        self.dydx_admin = DydxAdmin()
        self.chainlink_price_feed = ChainlinkPriceFeed()
        self.binance_client_obj = BinanceClient()
        self.price_floor_manager_obj = PriceFloorManager()
        self.firebase_data_manager_obj = FirebaseDataManager()
        self.dydx_client = dydx_client

    """ 
    method :: create_order -  is used to open and close orders on dydx. 
    params :: order_params - contains all the necessary parameter to open an order on dydx. 
    params :: dydx_client -  is a dydx client. with the help of this 
              client we perform operation on dydx it's different for the different asset. 
    """

    def create_order(self, order_params, dydx_client):
        dydx_order = DydxOrder()
        order_information = dydx_order.create_order(order_params, dydx_client)
        dydx_order_details = vars(order_information)
        dydx_order_details = dydx_order_details["data"]["order"]
        return dydx_order_details

    """ 
      method :: calculate_open_close_price -  is used to  calculate the open and close price for  orders on dydx. 
      params :: asset_pair - is the pair of asset such as ETH-USD,BTC-USD. 
      params :: eth_order_size -  it is the size of the order for which we have to calculate the open and close price.
      params :: symbol -  symbol is the sign for the asset ETH-USD,LINK-USD.
      """

    def calculate_open_close_price(self, asset_pair, eth_order_size, symbol):
        bids_consumed = 0
        dydx_order_obj = DydxOrder()
        asset_order_book = dydx_order_obj.get_order_book(
            market=asset_pair, dydx_client=self.dydx_client
        )
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

        price_floor = self.price_floor_manager_obj.get_asset_price_floor(
            AssetCodes.asset_name.value[asset_pair]
        )
        ema_data = self.firebase_data_manager_obj.fetch_data(
            collection_name="ema_data", document_name=symbol
        )

        ema = ema_data.get("ema")
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

    def create_order_params(self, side, market, size, market_price, dydx_client):
        if side == "SELL":
            market_price = int(market_price) + 10
        else:
            market_price = int(market_price) - 10
        dydx_admin = DydxAdmin()
        position_id = dydx_admin.get_position_id(dydx_client)
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
       method :: get_asset_price_and_size -  is used to get the total equity of an asset multiply by leverage and the market price of an asset.
       params :: asset_address - is the  chainlink Oracal address .
       params :: dydx_client -  is a dydx client. with the help of this client we perform operation on dydx it's different for the different asset.
       return :: asset total equity in dydx multiply by leverage  and the market price of the asset. 
    """

    def get_asset_price_and_size(self, asset_address, dydx_client):
        user = self.dydx_admin.get_account(dydx_client)
        user = vars(user)
        market_price = self.chainlink_price_feed.get_oracle_market_price(asset_address)
        total_volume = user["data"]["account"]["equity"]
        asset_volume = float(total_volume) / market_price
        asset_volume *= cruize_constants.POSITION_LEVERAGE
        asset_volume_with_leverage = str(
            round(asset_volume, cruize_constants.PRICE_ROUNDED_VALUE)
        )
        asset_details = {"price": market_price, "size": asset_volume_with_leverage}

        return asset_details

    """
          method :: compute_market_volatility -  is used compute the market volatility for an asset.
          params :: prices_data - an array of 6 months price data.
          return :: sigma ema and mu ema for an given asset price data.
    """

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

    """
          method :: market_volatility -  is used compute the market volatility for an asset.
          params :: symbol - symbol of an asset such as ETH-USD, BTC-USD.
     """

    def market_volatility(self, symbol):
        volatility_data = {}
        months_price_data = []
        price_data = self.firebase_data_manager_obj.fetch_sub_collections(
            collection="asset_price", document_name=symbol, sub_collection="prices"
        )

        if not price_data:
            # if db price data is none than  fetch prices for past 6 months .
            end_time = datetime.utcnow()
            start_time = end_time - relativedelta(months=6)
            months_price_data = self.binance_client_obj.price_data_per_interval(
                symbol=symbol,
                start_time=str(
                    start_time.timestamp() * cruize_constants.TIMESTAMP_MULTIPLIER
                ),
                end_time=str(
                    end_time.timestamp() * cruize_constants.TIMESTAMP_MULTIPLIER
                ),
            )
            volatility_data = self.compute_market_volatility(months_price_data)
        else:
            end_time = datetime.utcnow()
            start_time = datetime.utcnow() - timedelta(minutes=1)
            minutes_price_data = self.binance_client_obj.price_data_per_interval(
                symbol=symbol,
                end_time=str(
                    end_time.timestamp() * cruize_constants.TIMESTAMP_MULTIPLIER
                ),
                start_time=str(
                    start_time.timestamp() * cruize_constants.TIMESTAMP_MULTIPLIER
                ),
            )

            for month_price_data in price_data:
                month_price_data = month_price_data.to_dict()
                month_price_data = month_price_data["prices"].split(",")
                months_price_data.extend(month_price_data)

            # remove old price from the  list that should be equal to  new price's length  .
            del months_price_data[0 : len(minutes_price_data)]
            # append new prices to months_price_data array
            months_price_data.extend(minutes_price_data)
            # compute market volatility .
            volatility_data = self.compute_market_volatility(
                prices_data=months_price_data
            )

        total_month = 6
        data_size_for_month = int(len(months_price_data) / total_month)
        start_index = 0
        end_index = data_size_for_month

        for index in range(total_month):
            month_price_data = months_price_data[start_index:end_index]
            for idx, price in enumerate(month_price_data):
                price = round(float(price), 3)
                month_price_data[idx] = str(price)
            month_price_data_str = ",".join(month_price_data)

            self.firebase_data_manager_obj.store_sub_collections(
                collection="asset_price",
                sub_collection="prices",
                document_name=symbol,
                data={"prices": month_price_data_str},
                sub_document=f"month_{index+1}",
            )
            start_index = end_index
            end_index = end_index + data_size_for_month

        self.firebase_data_manager_obj.store_data(
            data={"ema": volatility_data}, document=symbol, collection_name="ema_data"
        )

    """
           method :: position_status -  is used to get open position status on dydx for an asset.
           params :: collection_name - collection for the asset ex ETHBUSD,BTCBUSD.
           params :: symbol -  symbol of an asset such as ETH-USD, BTC-USD.
           return ::  True if the short position is open on dydx  else False.
     """

    def position_status(self, collection_name, symbol):

        #  fetch data from db
        position_status = self.firebase_data_manager_obj.fetch_data(
            collection_name=collection_name, document_name=symbol
        )
        if position_status is None:
            #  if there is no data for asset on db than set data to db and return false.
            #  return false :  because as of now the position is not yet open on db.
            self.firebase_data_manager_obj.store_data(
                data={symbol: False}, document=symbol, collection_name=collection_name
            )
            return False
        return position_status[symbol]

    """
           method :: set_position_status -  is used to set open position status on dydx for an asset.
           params :: collection_name - collection for the asset ex ETHBUSD,BTCBUSD.
           params :: symbol -  symbol of an asset such as ETH-USD, BTC-USD.
           params :: status -  status of an position ex. True or false.
           return ::  None.
    """

    def set_position_status(self, collection_name, symbol, status):
        #  store data to db
        self.firebase_data_manager_obj.store_data(
            data={symbol: status}, document=symbol, collection_name=collection_name
        )

    def deposit_test_fund(self, dydx_client):
        dydx_p_client = dydx_client["dydx_instance"]
        return dydx_p_client.private.request_testnet_tokens()

    """
            method :: deposit_to_dydx -  is used to deposit USDC to dydx.
            params :: amount - USDC value in number.
            params ::dydx_client -  is a dydx client. with the help of this client we perform operation on dydx it's different for the different asset.
            return ::  transaction hash for deposit transaction.
     """

    def deposit_to_dydx(self, amount, dydx_client):
        try:
            dydx_p_client = dydx_client["dydx_instance"]
            transaction_manager = TransactionManager()
            transaction = transaction_manager.build_transaction(
                wallet_address=cruize_constants.WALLET_ADDRESS
            )
            position_id = dydx_p_client.get_position_id(dydx_client)
            tnx_hash = dydx_p_client.eth.deposit_to_exchange(
                position_id=position_id, human_amount=amount, send_options=transaction
            )

            return tnx_hash
        except Exception as e:
            raise Exception(e)

    """
             method :: withdraw_from_dydx -  is used to withdraw USDC from dydx.
             params :: recipient_address - the account in which we want to withdraw fund.
             params ::dydx_client -  is a dydx client. with the help of this client we perform operation on dydx it's different for the different asset.
             return ::  transaction hash for deposit transaction.
      """

    def withdraw_from_dydx(self, recipient_address, dydx_client):
        try:
            dydx_p_client = dydx_client["dydx_instance"]
            transaction_manager = TransactionManager()
            transaction = transaction_manager.build_transaction(
                wallet_address=cruize_constants.WALLET_ADDRESS
            )
            tnx_hash = dydx_p_client.eth.withdraw_to(
                recipient=recipient_address, send_options=transaction
            )
            return tnx_hash
        except Exception as e:
            raise Exception(e)

    """ 
      method :: open_order_on_dydx -  is used to open orders on dydx. it has  algorithm to open order's on dydx  
      params :: order_details - contains all the necessary parameter to open an order on dydx. 
      """

    def open_order_on_dydx(self, order_details):
        dydx_asset_instance = asset_dydx_instance[order_details["asset_pair"]]
        dydx_order_manager = DydxOrderManager(dydx_asset_instance)
        is_position_open = dydx_order_manager.position_status(
            "position_status", order_details["binance_asset_pair"]
        )
        data = dydx_order_manager.get_asset_price_and_size(
            order_details["asset_oracle_address"], dydx_asset_instance
        )
        asset_market_price = data["price"]

        asset_position_size = data["size"]

        if order_details["asset_trigger_price"] is None:

            asset_trigger_price = dydx_order_manager.calculate_open_close_price(
                asset_pair=order_details["asset_pair"],
                eth_order_size=float(asset_position_size),
                symbol=order_details["binance_asset_pair"],
            )
        else:
            asset_trigger_price = asset_market_price + 10
        if is_position_open is False:

            if asset_trigger_price >= asset_market_price:
                order_params = dydx_order_manager.create_order_params(
                    order_details["order_side"],
                    order_details["asset_pair"],
                    asset_position_size,
                    asset_market_price,
                    dydx_asset_instance,
                )
                dydx_order_manager.create_order(order_params, dydx_asset_instance)
                is_position_open = True
                dydx_order_manager.set_position_status(
                    collection_name="position_status",
                    symbol=order_details["binance_asset_pair"],
                    status=is_position_open,
                )
                print(
                    f"DydxOrderManager:: {order_details['asset_pair']} - Short position is open"
                )
            else:
                print(
                    f"DydxOrderManager:: { order_details['asset_pair']} {asset_trigger_price} is less than market price {asset_market_price}"
                )
        else:
            if asset_trigger_price >= asset_market_price:
                print(f"{order_details['asset_pair']} position is already open")
            else:
                print(
                    f"DydxOrderManager:: {order_details['asset_pair']} trigger price {asset_trigger_price} is less than market price {asset_market_price}"
                )

    def close_order_on_dydx(self, order_details):
        dydx_asset_instance = asset_dydx_instance[order_details["asset_pair"]]
        dydx_order_manager = DydxOrderManager(dydx_asset_instance)
        is_position_open = dydx_order_manager.position_status(
            "position_status", order_details["binance_asset_pair"]
        )
        data = dydx_order_manager.get_asset_price_and_size(
            order_details["asset_oracle_address"], dydx_asset_instance
        )
        asset_market_price = data["price"]
        asset_position_size = data["size"]

        if order_details["asset_trigger_price"] is None:
            asset_trigger_price = dydx_order_manager.calculate_open_close_price(
                asset_pair=order_details["asset_pair"],
                eth_order_size=float(asset_position_size),
                symbol=order_details["binance_asset_pair"],
            )
        else:
            asset_trigger_price = asset_market_price - 10
        if is_position_open is True:
            if asset_trigger_price < asset_market_price:
                order_params = dydx_order_manager.create_order_params(
                    order_details["order_side"],
                    order_details["asset_pair"],
                    asset_position_size,
                    asset_market_price,
                    dydx_asset_instance,
                )
                dydx_order_manager.create_order(order_params, dydx_asset_instance)
                is_position_open = False
                dydx_order_manager.set_position_status(
                    collection_name="position_status",
                    symbol=order_details["binance_asset_pair"],
                    status=is_position_open,
                )

                print(
                    f"class::DydxOrderManager {order_details['asset_pair']} - Short position is closed"
                )
            else:
                print(
                    f"DydxOrderManager:: {order_details['asset_pair']} trigger price {asset_trigger_price} is greater than market price {asset_market_price}"
                )
        else:
            if asset_trigger_price < asset_market_price:
                print(
                    f"DydxOrderManager:: {order_details['asset_pair']} short position is closed"
                )
            else:
                print(
                    f"DydxOrderManager::{order_details['asset_pair']} trigger price {asset_trigger_price} is less than market price {asset_market_price}"
                )


if __name__ == "__main__":
    a = DydxOrderManager(None)
    a.market_volatility("ETHBUSD")
