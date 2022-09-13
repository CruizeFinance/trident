import time
from components import OrderManager
from services import DydxWithdrawal, LoadContracts, DydxOrder, DydxAdmin
from tests.constants import SEVEN_DAYS_S
from settings_config.celery_config import app

open_position = False
order_id = "5d90fda25c94f91a85a3b8bf3081a09be442e00941ed11c5b31c6dc890cc464"


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
        print(open_position)
        load_contract = LoadContracts()
        market_price = load_contract.get_asset_price(
            "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
        )  # make it dynamic
        print(market_price)
        trigger_price = 1750
        if trigger_price >= market_price:
            try:
                dydx_order = DydxOrder()
                admin = DydxAdmin()
                position_id = admin.get_position_id()
                user = admin.get_account()
                user = vars(user)
                user_balance = user["data"]["account"]["quoteBalance"]
                print(user_balance)
                size = float(user_balance) / market_price
                print("ve", size)
                size *= 5

                order_manager = OrderManager()

                order_information = dydx_order.create_order(
                    {
                        "position_id": position_id,  # make it dynamic
                        "market": "ETH-USD",  # make it dynamic
                        "side": "SELL",
                        "order_type": "MARKET",
                        "post_only": "false",
                        "size": str(round(size, 3)),  # make it dynamic
                        "price": "1600",  # make it dynac
                        "limit_fee": "0.4",
                        "expiration_epoch_seconds": time.time() + SEVEN_DAYS_S + 60,
                        "time_in_force": "IOC",
                    }
                )
                dydx_order_details = vars(order_information)
                dydx_order_details = dydx_order_details["data"]["order"]
                order_manager.store_data(dydx_order_details, "dydx_orders")
                order_id = dydx_order_details["id"]
                print("order data-->", dydx_order_details)
                open_position = True
            except Exception as e:
                print("this is error", vars(e))
    else:
        print("order is already placed")


@app.task(name="close_order_on_dydx", default_retry_delay=4 * 60)
def close_order_on_dydx():
    global open_position
    global order_id

    if open_position is True:
        print(open_position)
        load_contract = LoadContracts()
        market_price = load_contract.get_asset_price(
            "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
        )  # make it dynamic
        print(market_price)
        trigger_price = 1600
        if trigger_price < market_price:
            try:
                dydx_order = DydxOrder()
                admin = DydxAdmin()
                position_id = admin.get_position_id()
                user = admin.get_account()
                user = vars(user)
                user_balance = user["data"]["account"]["equity"]
                print(user_balance)
                size = float(user_balance) / market_price
                print("ve", size)
                size *= 5

                order_manager = OrderManager()

                order_information = dydx_order.create_order(
                    {
                        "position_id": position_id,
                        "market": "ETH-USD",
                        "side": "BUY",
                        "order_type": "MARKET",
                        "post_only": "false",
                        "size": str(round(size, 3)),
                        "price": str(int(market_price + 10)),
                        "limit_fee": "0.4",
                        "expiration_epoch_seconds": time.time() + SEVEN_DAYS_S + 60,
                        "time_in_force": "IOC",
                    }
                )
                dydx_order_details = vars(order_information)
                dydx_order_details = dydx_order_details["data"]["order"]
                order_manager.store_data(dydx_order_details, "dydx_orders")
                order_id = dydx_order_details["id"]
                print("order data-->", dydx_order_details)
                open_position = False
            except Exception as e:
                print("this is error", vars(e))
    else:
        print("order is already placed")
