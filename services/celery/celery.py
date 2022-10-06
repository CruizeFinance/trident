from dydx3 import constants
from components import FirebaseDataManager
from components.dydx_order_manager import DydxOrderManager
from services import DydxWithdrawal
from settings_config.celery_config import app
from utilities import cruize_constants
from utilities.utills import Utilities
#need to store on db
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
def open_order_on_dydx(eth_trigger_price=None, btc_tigger_price=None):
    global eth_open_position
    global btc_open_position
    utilities = Utilities()
    data = utilities.get_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, 100
    )
    eth_market_price = data["market_price"]
    # we have to change this with the actual btc volume
    eth_position_size = data["size"]
    data = utilities.get_price_and_size(
        cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS, 100
    )
    btc_market_price = data["market_price"]
    btc_position_size = data["size"]
    # TODO: write a formula to calculate  the trigger_price
    if eth_trigger_price and btc_tigger_price is None:
        # here we will keep our trigger price formulas
        eth_trigger_price = 900
        btc_tigger_price = 1000
    else:
        # for_testing
        eth_trigger_price = eth_market_price + 10
        btc_tigger_price = btc_market_price + 10

    if eth_open_position is False:
        if eth_trigger_price >= eth_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = utilities.create_order_params(
                constants.ORDER_SIDE_SELL,
                constants.MARKET_ETH_USD,
                eth_position_size,
                eth_market_price,
            )
            dydx_order_manager.create_order(order_params)
            eth_open_position = True
            utilities.print_status_for_order(
                cruize_constants.ETH, cruize_constants.POSITION_OPEN
            )

    else:
        utilities.print_orders_status(
            cruize_constants.ETH,
            eth_market_price,
            eth_trigger_price,
            cruize_constants.POSITION_OPEN,
        )
    if btc_open_position is False:
        if btc_tigger_price >= btc_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = utilities.create_order_params(
                constants.ORDER_SIDE_SELL,
                constants.MARKET_BTC_USD,
                btc_position_size,
                btc_market_price,
            )
            dydx_order_manager.create_order(order_params)
            btc_open_position = True
            utilities.print_status_for_order(
                cruize_constants.BTC, cruize_constants.POSITION_OPEN
            )

        else:
            utilities.print_orders_status(
                cruize_constants.BTC,
                btc_market_price,
                btc_tigger_price,
                cruize_constants.POSITION_OPEN,
            )


@app.task(name="close_order_on_dydx", default_retry_delay=4 * 60)
def close_order_on_dydx(eth_trigger_price=None, btc_tigger_price=None):
    global eth_open_position
    global btc_open_position
    utilities = Utilities()
    data = utilities.get_price_and_size(
        cruize_constants.TEST_ETH_USD_ORACLE_ADDRESS, 1000
    )
    eth_market_price = data["market_price"]
    # we have to change this with the actual btc volume
    eth_position_size = data["size"]
    data = utilities.get_price_and_size(
        cruize_constants.TEST_BTC_USD_ORACLE_ADDRESS, 1000
    )
    btc_market_price = data["market_price"]
    btc_position_size = data["size"]
    # TODO: write a formula to calculate  the trigger_price
    trigger_price = ""
    if eth_trigger_price and btc_tigger_price is None:
        eth_trigger_price = 2000
        btc_tigger_price = 1000
    else:
        # for testing
        eth_trigger_price = eth_market_price - 10
        btc_tigger_price = btc_market_price - 10

    if eth_open_position is True:
        if eth_trigger_price < eth_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = utilities.create_order_params(
                constants.ORDER_SIDE_BUY,
                constants.MARKET_ETH_USD,
                eth_position_size,
                eth_market_price,
            )
            dydx_order_manager.create_order(order_params)
            eth_open_position = False
            utilities.print_status_for_order(
                cruize_constants.ETH, cruize_constants.POSITION_CLOSED
            )

    else:
        utilities.print_orders_status(
            cruize_constants.ETH,
            eth_market_price,
            eth_trigger_price,
            cruize_constants.POSITION_CLOSED,
        )
    if btc_open_position is True:
        if btc_tigger_price < btc_market_price:
            dydx_order_manager = DydxOrderManager()
            order_params = utilities.create_order_params(
                constants.ORDER_SIDE_BUY,
                constants.MARKET_BTC_USD,
                btc_position_size,
                btc_market_price,
            )
            dydx_order_manager.create_order(order_params)
            btc_open_position = False
            utilities.print_status_for_order(
                cruize_constants.BTC, cruize_constants.POSITION_CLOSED
            )
        else:
            utilities.print_orders_status(
                cruize_constants.BTC,
                btc_market_price,
                btc_tigger_price,
                cruize_constants.POSITION_CLOSED,
            )


if __name__ == "__main__":
    close_order_on_dydx()
