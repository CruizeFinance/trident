import time
from components import OrderManager
from services import DydxWithdrawal, DydxOrder, DydxAdmin
from tests.constants import SEVEN_DAYS_S
from settings_config.celery_config import app

open_position = False


@app.task(name="check_withdrawal", default_retry_delay=4 * 60)
def check_withdrawal():
    dydx_withdrawal_obj = DydxWithdrawal()
    order_manager_obj = OrderManager()
    result = dydx_withdrawal_obj.all_transfer_details(
        {"limit": 100, "transfer_type": "WITHDRAWAL"}
    )
    transfers = result["data"]["transfers"]
    for transfer in transfers:
        if transfer["status"] == "CONFIRMED":
            order_manager_obj.update_data(transfer["id"], "withdrawal", "CONFIRMED")


@app.task(name="open_order_on_dydx", track_started=True)
def open_order_on_dydx(trigger_price_test=None):
    global open_position
    global order_id
    order_manager_obj = OrderManager()
    order_params = order_manager_obj.order_params()
    market_price = order_params["market_price"]
    trigger_price_test = 1100
    if trigger_price_test is None:
        # we can put the math formula here for trigger price .
        trigger_price = trigger_price_test
    else:
        trigger_price = market_price + 100
    if open_position is False:
        # TODO: write a formula to calculate  the trigger_price

        if trigger_price >= market_price:

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
                    "price": str(int(market_price - 100)),
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
            print("SELL order is  placed")

    else:
        if trigger_price >= market_price:
            print("SELL order is already placed")
        else:
            print(f"market price ${market_price} grater than ${trigger_price}")


@app.task(name="close_order_on_dydx", default_retry_delay=4 * 60)
def close_order_on_dydx(trigger_price=None):
    global open_position
    global order_id
    order_manager_obj = OrderManager()
    order_params = order_manager_obj.order_params()
    market_price = order_params["market_price"]
    # TODO: write a formula to calculate  the trigger_price
    trigger_price = ""
    if trigger_price is None:
        trigger_price = 1100
    else:
        trigger_price = market_price - 100
    if open_position is True:

        if trigger_price < market_price:

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
                    "price": str(int(market_price + 10)),
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
            print("BUY order is  placed")

    else:
        if trigger_price < market_price:
            print("Buy order is already placed")
        else:
            print(f"market price ${market_price} less than ${trigger_price}")
