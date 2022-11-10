import time

from dydx3 import constants
from components import FirebaseDataManager, PriceFloorManager
from components.dydx_order_manager import DydxOrderManager
from services import DydxWithdrawal
from services.avve_asset_apy import AaveApy
from settings_config import asset_dydx_instance
from settings_config.celery_config import app
from utilities import cruize_constants


# TODO : need to store on db fetch from db as well


@app.task(name="check_withdrawal", default_retry_delay=4 * 60)
def check_withdrawal():

    dydx_withdrawal_obj = DydxWithdrawal(asset_dydx_instance["BTC-USD"])
    order_manager_obj = FirebaseDataManager()
    result = dydx_withdrawal_obj.all_transfer_details(
        {"limit": 100, "transfer_type": "WITHDRAWAL"},
    )
    transfers = result["data"]["transfers"]
    for transfer in transfers:
        if transfer["status"] == "CONFIRMED":
            order_manager_obj.update_data(
                transfer["id"], "withdrawal", {"status": "CONFIRMED"}
            )
            # need to send an notification for the order conformation


## For ETH
@app.task(name="open_eth_order_on_dydx", track_started=True)
def open_eth_order_on_dydx(eth_trigger_price=None):
    print("Start::open eth order on dydx")
    dydx_order_manager_obj = DydxOrderManager()
    asset_details = {
        "asset_trigger_price": None,
        "asset_pair": "ETH-USD",
        "binance_asset_pair": "ETHBUSD",
        "order_side": "SELL",
        "asset_oracle_address": cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS,
    }
    if eth_trigger_price is not None:
        asset_details["asset_trigger_price"] = 0
    dydx_order_manager_obj.open_order_on_dydx(asset_details)


# For ETH
@app.task(name="close_eth_order_on_dydx", default_retry_delay=4 * 60)
def close_eth_order_on_dydx(
    eth_trigger_price=None,
):
    print("Start::close eth order on dydx")
    dydx_order_manager_obj = DydxOrderManager()
    asset_details = {
        "asset_trigger_price": None,
        "asset_pair": "ETH-USD",
        "binance_asset_pair": "ETHBUSD",
        "order_side": "BUY",
        "asset_oracle_address": cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS,
    }
    if eth_trigger_price is not None:
        asset_details["asset_trigger_price"] = 0
    dydx_order_manager_obj.close_order_on_dydx(asset_details)


# BTC --> positions
@app.task(name="open_btc_order_on_dydx", track_started=True)
def open_btc_order_on_dydx(btc_trigger_price=None):
    print("Start::open btc order on dydx")
    dydx_order_manager_obj = DydxOrderManager()
    asset_details = {
        "asset_trigger_price": None,
        "asset_pair": "BTC-USD",
        "binance_asset_pair": "BTCBUSD",
        "order_side": "SELL",
        "asset_oracle_address": cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS,
    }
    if btc_trigger_price is not None:
        asset_details["asset_trigger_price"] = 0
    dydx_order_manager_obj.open_order_on_dydx(asset_details)


@app.task(name="close_btc_order_on_dydx", default_retry_delay=4 * 60)
def close_btc_order_on_dydx(btc_trigger_price=None):
    print("Start::close btc order on dydx")
    dydx_order_manager_obj = DydxOrderManager()
    asset_details = {
        "asset_trigger_price": None,
        "asset_pair": "BTC-USD",
        "binance_asset_pair": "BTCBUSD",
        "order_side": "BUY",
        "asset_oracle_address": cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS,
    }
    if btc_trigger_price is not None:
        asset_details["asset_trigger_price"] = 0
    dydx_order_manager_obj.close_order_on_dydx(asset_details)


@app.task(
    name="compute_eth_usdc_volatility",
)
def compute_eth_usdc_volatility():
    print("Start::compute_eth_usdc_volatility")
    current_time = time.time()
    print("compute_eth_usdc_volatility", current_time)
    dydx_order_manager_obj = DydxOrderManager(asset_dydx_instance["ETH-USD"])
    dydx_order_manager_obj.market_volatility(symbol="ETHBUSD")
    print("End::compute_eth_usdc_volatility")
    end_time = time.time()
    print("compute_eth_usdc_volatility", end_time)
    print("time all", end_time - current_time)


@app.task(
    name="compute_btc_usdc_volatility",
)
def compute_btc_usdc_volatility():
    print("Start::compute_btc_usdc_volatility")
    dydx_order_manager_obj = DydxOrderManager(asset_dydx_instance["BTC-USD"])
    dydx_order_manager_obj.market_volatility(symbol="BTCBUSD")
    print("End::compute_btc_usdc_volatility")


# TODO: set price floor for other asset's too.
@app.task(
    name="set_price_floor",
)
def set_price_floor():
    print("set_price_floor :: Setting price floor")
    price_floor_manager_obj = PriceFloorManager()
    price_floor_manager_obj.set_price_floor("ethereum")
    price_floor_manager_obj.set_price_floor("bitcoin")


@app.task(name="store_asset_apy")
def store_asset_apys():
    print("store_asset_apys :: Setting apy")
    asset_apy_obj = AaveApy()
    asset_apys = asset_apy_obj.fetch_asset_apys()
    asset_apy_obj.store_asset_apys(asset_apys)


if __name__ == "__main__":
    compute_eth_usdc_volatility()
