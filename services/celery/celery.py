from dydx3 import constants
from components import FirebaseDataManager, PriceFloorManager
from components.dydx_order_manager import DydxOrderManager
from services import DydxWithdrawal
from settings_config.celery_config import app
from utilities import cruize_constants


# TODO : need to store on db fetch from db as well



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

    dydx_order_manager = DydxOrderManager()

    eth_open_position = dydx_order_manager.position_status('position_status', "ETHBUSD")
    btc_open_position = dydx_order_manager.position_status('position_status', "BTCBUSD")
    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, 100
    )
    eth_market_price = data["price"]
    # we have to change this with the actual btc volume
    eth_position_size = data["size"]
    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS, 100
    )
    btc_market_price = data["price"]
    btc_position_size = data["size"]
    # TODO: write a formula to calculate  the trigger_price
    if eth_trigger_price and btc_trigger_price is None:
        # here we will keep our trigger price formulas
        #  TODO:size must  change of ETH and BTC .
        #   size of ETH AND BTC must be equal to the staked asset to cruize protocol.
        size = 10
        eth_trigger_price = dydx_order_manager.calculate_open_close_price(
            "ETH-USD", size, "ETHBUSD"
        )
        btc_trigger_price = dydx_order_manager.calculate_open_close_price(
            "BTC-USD", size, "BTCBUSD"
        )
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
            dydx_order_manager.set_position_status(collection_name="position_status", symbol="ETHBUSD",
                                                   status=eth_open_position)
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
            dydx_order_manager.set_position_status(collection_name="position_status", symbol="BTCBUSD",
                                                   status=btc_open_position)
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
    dydx_order_manager = DydxOrderManager()
    eth_open_position = dydx_order_manager.position_status('position_status', "ETHBUSD")
    btc_open_position = dydx_order_manager.position_status('position_status', "BTCBUSD")

    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, 1000
    )
    eth_market_price = data["price"]
    # we have to change this with the actual btc volume
    eth_position_size = data["size"]

    data = dydx_order_manager.get_asset_price_and_size(
        cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS, 1000
    )
    btc_market_price = data["price"]
    btc_position_size = data["size"]

    if eth_trigger_price and btc_trigger_price is None:
        # TODO:size must  change of ETH and BTC .
        #  size of ETH AND BTC must be equal to the staked asset to cruize protocol.
        size = 10
        eth_trigger_price = dydx_order_manager.calculate_open_close_price(
            "ETH-USD", size, "ETHBUSD"
        )
        btc_trigger_price = dydx_order_manager.calculate_open_close_price(
            "BTC-USD", size, "BTCBUSD"
        )
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
            dydx_order_manager.set_position_status(collection_name="position_status", symbol="ETHBUSD",
                                                   status=eth_open_position)
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
            dydx_order_manager.set_position_status(collection_name="position_status",symbol="BTCBUSD",status=btc_open_position)
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
    dydx_order_manager_obj.market_volatility(symbol="ETHBUSD")


@app.task(
    name="computer_btc_usdc_volatility",
)
def computer_btc_usdc_volatility():
    dydx_order_manager_obj = DydxOrderManager()
    dydx_order_manager_obj.market_volatility(symbol="BTCBUSD")


# TODO: set price floor for other asset's too.
@app.task(
    name="set_price_floor",
)
def set_price_floor():
    price_floor_manager_obj = PriceFloorManager()
    price_floor_manager_obj.set_price_floor("ethereum")
    price_floor_manager_obj.set_price_floor("bitcoin")


if __name__ == "__main__":
    computer_eth_usdc_volatility()
