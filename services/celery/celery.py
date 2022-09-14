import time
from components import OrderManager
from services import DydxWithdrawal, LoadContracts, DydxOrder, DydxAdmin
from tests.constants import SEVEN_DAYS_S
from settings_config.celery_config import app

open_position = True


@app.task(name="check_withdrawal", default_retry_delay=4 * 60)
def check_withdrawal():
    dydx_withdrawal = DydxWithdrawal()
    order_manager = OrderManager()
    result = dydx_withdrawal.all_transfer_details(
        {"limit": 100, "transfer_type": "WITHDRAWAL"}
    )
    transfers = result["data"]["transfers"]
    for transfer in transfers:
        if transfer["status"] == "CONFIRMED":
            order_manager.update_data(transfer["id"], "withdrawal", "CONFIRMED")


@app.task(name="open_order_on_dydx", track_started=True)
def open_order_on_dydx():
    global open_position
    global order_id
    if open_position is False:
        # TODO: set formula for trigger_price
        load_contract = LoadContracts()
        order_params = load_contract.order_params()
        trigger_price = 1750
        if trigger_price >= order_params["market_price"]:
            try:
                dydx_order = DydxOrder()
                order_manager = OrderManager()
                order_information = dydx_order.create_order(
                    {
                        "position_id": order_params["position_id"],
                        "market": "ETH-USD",
                        "side": "SELL",
                        "order_type": "MARKET",
                        "post_only": "false",
                        "size": order_params["size"],
                        "price": str(int(order_params["market_price"] - 100)),
                        "limit_fee": "0.4",
                        "expiration_epoch_seconds": time.time() + SEVEN_DAYS_S + 60,
                        "time_in_force": "IOC",
                    }
                )
                dydx_order_details = vars(order_information)
                dydx_order_details = dydx_order_details["data"]["order"]
                order_manager.store_data(dydx_order_details, "dydx_orders")
                order_id = dydx_order_details["id"]
                open_position = True
            except Exception as e:
                print("this is error", vars(e))
    else:
        print("SELL order is already placed")


@app.task(name="close_order_on_dydx", default_retry_delay=4 * 60)
def close_order_on_dydx():
    global open_position
    global order_id

    if open_position is True:

        load_contract = LoadContracts()
        order_params = load_contract.order_params()
        # TODO: set formula for trigger_price
        trigger_price = 1600
        if trigger_price < order_params["market_price"]:
            try:
                dydx_order = DydxOrder()
                order_manager = OrderManager()
                order_information = dydx_order.create_order(
                    {
                        "position_id": order_params["position_id"],
                        "market": "ETH-USD",
                        "side": "BUY",
                        "order_type": "MARKET",
                        "post_only": "false",
                        "size": order_params["size"],
                        "price": str(int(order_params["market_price"] + 10)),
                        "limit_fee": "0.4",
                        "expiration_epoch_seconds": time.time() + SEVEN_DAYS_S + 60,
                        "time_in_force": "IOC",
                    }
                )
                open_position = False
                dydx_order_details = vars(order_information)
                dydx_order_details = dydx_order_details["data"]["order"]
                order_manager.store_data(dydx_order_details, "dydx_orders")
                order_id = dydx_order_details["id"]

            except Exception as e:
                print(vars(e))
    else:
        print("BUY order is already placed")
