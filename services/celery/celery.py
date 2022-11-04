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
@app.task(name="open_order_on_dydx", track_started=True)
def open_order_on_dydx(eth_trigger_price=None):
    print("Start::open_order_on_dydx")
    dydx_eth_instance = asset_dydx_instance["ETH-USD"]
    dydx_order_manager = DydxOrderManager(asset_dydx_instance["ETH-USD"])
    eth_open_position = dydx_order_manager.position_status("position_status", "ETHBUSD")
    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, dydx_eth_instance
    )
    eth_market_price = data["price"]
    # we have to change this with the actual btc volume
    eth_position_size = data["size"]

    # TODO: write a formula to calculate  the trigger_price

    if eth_trigger_price is None:
        # here we will keep our trigger price formulas
        #  TODO:size must  change of ETH and BTC .
        #   size of ETH AND BTC must be equal to the staked asset to cruize protocol.
        print("Start::calculate open close")
        eth_trigger_price = dydx_order_manager.calculate_open_close_price(
            asset_pair="ETH-USD",
            eth_order_size=float(eth_position_size),
            symbol="ETHBUSD",
        )

    else:
        eth_trigger_price = eth_market_price + 10

    if eth_open_position is False:
        if eth_trigger_price >= eth_market_price:
            order_params = dydx_order_manager.create_order_params(
                constants.ORDER_SIDE_SELL,
                constants.MARKET_ETH_USD,
                eth_position_size,
                eth_market_price,
                dydx_eth_instance,
            )
            dydx_order_manager.create_order(order_params, dydx_eth_instance)
            eth_open_position = True
            dydx_order_manager.set_position_status(
                collection_name="position_status",
                symbol="ETHBUSD",
                status=eth_open_position,
            )
            print("ETH - Short position is open")
        else:
            print(
                f"eth trigger price {eth_trigger_price} is less than market price {eth_market_price}"
            )
    else:
        if eth_trigger_price >= eth_market_price:
            print("ETH position is already open")
        else:
            print(
                f"eth trigger price {eth_trigger_price} is less than market price {eth_market_price}"
            )


# For ETH
@app.task(name="close_order_on_dydx", default_retry_delay=4 * 60)
def close_order_on_dydx(eth_trigger_price=None, btc_trigger_price=None):
    print("Start::close order on dydx")
    dydx_order_manager = DydxOrderManager(asset_dydx_instance["ETH-USD"])
    eth_open_position = dydx_order_manager.position_status("position_status", "ETHBUSD")

    dydx_eth_instance = asset_dydx_instance["ETH-USD"]

    asset_data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, dydx_eth_instance
    )
    eth_market_price = asset_data["price"]
    # we have to change this with the actual btc volume
    eth_position_size = asset_data["size"]

    if eth_trigger_price and btc_trigger_price is None:

        eth_trigger_price = dydx_order_manager.calculate_open_close_price(
            "ETH-USD", eth_position_size, "ETHBUSD"
        )

    else:
        # for testing
        eth_trigger_price = eth_market_price - 10

    if eth_open_position is True:
        if eth_trigger_price < eth_market_price:

            order_params = dydx_order_manager.create_order_params(
                constants.ORDER_SIDE_BUY,
                constants.MARKET_ETH_USD,
                eth_position_size,
                eth_market_price,
                dydx_eth_instance,
            )
            dydx_order_manager.create_order(order_params, dydx_eth_instance)
            eth_open_position = False
            dydx_order_manager.set_position_status(
                collection_name="position_status",
                symbol="ETHBUSD",
                status=eth_open_position,
            )
            print("ETH - Short position is Closed")
        else:
            print(
                f"ETH trigger price {eth_trigger_price} is less than market price {eth_market_price}"
            )
    else:
        if eth_trigger_price >= eth_market_price:
            print("ETH- short position is already Closed")
        else:
            print(
                f"ETH trigger price {eth_trigger_price} is less than market price {eth_market_price}"
            )


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
