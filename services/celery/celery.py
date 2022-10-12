from dydx3 import constants
from components import FirebaseDataManager
from components.dydx_order_manager import DydxOrderManager
from services import DydxWithdrawal
from services.binance_client.binance_client import BinanceClient
from settings_config.celery_config import app
from utilities import cruize_constants
import numpy
import pandas

# need to store on db
eth_open_position = False
btc_open_position = False


@app.task(name="check_withdrawal", default_retry_delay=4 * 60)
def check_withdrawal():
    dydx_withdrawal_obj = DydxWithdrawal()
    order_manager_obj = FirebaseDataManager()
    result = dydx_withdrawal_obj.all_transfer_details(
        {"limit": 100, "transfer_type": "WITHDRAWAL"}
    )
    transfers = result["data"]["transfers"]
    for transfer in transfers:
        if transfer["status"] == "CONFIRMED":
            order_manager_obj.update_data(transfer["id"], "withdrawal", "CONFIRMED")
            # need to send an notification for the order conformation


@app.task(name="open_order_on_dydx", track_started=True)
def open_order_on_dydx(eth_trigger_price=None, btc_trigger_price=None):
    global eth_open_position
    global btc_open_position
    dydx_order_manager = DydxOrderManager()
    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, 100
    )
    eth_market_price = data["market_price"]
    # we have to change this with the actual btc volume
    eth_position_size = data["size"]
    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS, 100
    )
    btc_market_price = data["market_price"]
    btc_position_size = data["size"]
    # TODO: write a formula to calculate  the trigger_price
    if eth_trigger_price and btc_trigger_price is None:
        # here we will keep our trigger price formulas
        eth_trigger_price = 900
        btc_trigger_price = 1000
    else:
        # for_testing
        eth_trigger_price = eth_market_price + 10
        btc_trigger_price = btc_market_price + 10

    if eth_open_position is False:
        if eth_trigger_price >= eth_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = dydx_order_manager.create_order_params(
                constants.ORDER_SIDE_SELL,
                constants.MARKET_ETH_USD,
                eth_position_size,
                eth_market_price,
            )
            dydx_order_manager.create_order(order_params)
            eth_open_position = True
            print("ETH - Short position is open")

        else:
            if eth_trigger_price >= eth_market_price:
                print("ETH position is already open")
            else:
                print(
                    f"eth trigger price {eth_trigger_price} is less than market price {eth_market_price}"
                )
    if btc_open_position is False:
        if btc_trigger_price >= btc_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = dydx_order_manager.create_order_params(
                constants.ORDER_SIDE_SELL,
                constants.MARKET_BTC_USD,
                btc_position_size,
                btc_market_price,
            )
            dydx_order_manager.create_order(order_params)
            btc_open_position = True
            print("BTC - Short position is open")
        else:
            if btc_trigger_price >= btc_market_price:
                print("BTC- short position is already open")
            else:
                print(
                    f"BTC trigger price {btc_trigger_price} is less than market price {btc_market_price}"
                )


@app.task(name="close_order_on_dydx", default_retry_delay=4 * 60)
def close_order_on_dydx(eth_trigger_price=None, btc_trigger_price=None):
    global eth_open_position
    global btc_open_position
    dydx_order_manager = DydxOrderManager()
    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, 1000
    )
    eth_market_price = data["market_price"]
    # we have to change this with the actual btc volume
    eth_position_size = data["size"]
    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS, 1000
    )
    btc_market_price = data["market_price"]
    btc_position_size = data["size"]

    if eth_trigger_price and btc_trigger_price is None:
        # TODO:size must be change of ETH and BTC
        size = 10
        eth_trigger_price = dydx_order_manager.calculate_open_close_price('ETH-USD',size,'ETHBUSD')
        btc_trigger_price =dydx_order_manager.calculate_open_close_price('BTC-USD',size,'BTCBUSD')
    else:
        # for testing
        eth_trigger_price = eth_market_price - 10
        btc_trigger_price = btc_market_price - 10

    if eth_open_position is True:
        if eth_trigger_price < eth_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = dydx_order_manager.create_order_params(
                constants.ORDER_SIDE_BUY,
                constants.MARKET_ETH_USD,
                eth_position_size,
                eth_market_price,
            )
            dydx_order_manager.create_order(order_params)
            eth_open_position = False
            print("ETH - Short position is Closed")

        else:
            if eth_trigger_price >= eth_market_price:
                print("ETH- short position is already Closed")
            else:
                print(
                    f"ETH trigger price {eth_trigger_price} is less than market price {eth_market_price}"
                )

    if btc_open_position is True:
        if btc_trigger_price < btc_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = dydx_order_manager.create_order_params(
                constants.ORDER_SIDE_BUY,
                constants.MARKET_BTC_USD,
                btc_position_size,
                btc_market_price,
            )
            dydx_order_manager.create_order(order_params)
            btc_open_position = False
            print("BTC - Short position is Closed")
        else:
            if btc_trigger_price >= btc_market_price:
                print("BTC- short position is already Closed")
            else:
                print(
                    f"BTC trigger price {btc_trigger_price} is less than market price {btc_market_price}"
                )


@app.task(
    name="computer_eth_usdc_volatility",
)
def computer_eth_usdc_volatility():
    dydx_order_manager_obj = DydxOrderManager()
    dydx_order_manager_obj.market_volatility(symbol="ETHUSDC")

@app.task(
    name="computer_btc_usdc_volatility",
)
def computer_btc_usdc_volatility():
    dydx_order_manager_obj = DydxOrderManager()
    dydx_order_manager_obj.market_volatility(symbol="BTCUSDC")
if __name__ == "__main__":
    computer_eth_usdc_volatility()
