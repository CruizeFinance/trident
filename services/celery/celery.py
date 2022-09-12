import time
from components import OrderManager
from services import DydxWithdrawal, LoadContracts, DydxOrder, DydxAdmin
from tests.constants import SEVEN_DAYS_S
from settings_config.celery_config import app

open_position = False
order_id = None


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
        load_contract = LoadContracts()
        market_price = load_contract.get_asset_price(
            "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
        )  # make it dynamic
        trigger_price = 1750
        if trigger_price >= market_price:
            try:
                dydx_order = DydxOrder()
                admin = DydxAdmin()
                position_id = admin.get_position_id()
                user =  admin.get_account()
                user_balance = user['freeCollateral']
                size = user_balance/market_price
                order_manager = OrderManager()
                order_information = dydx_order.create_order(
                    {
                        "position_id": position_id,  # make it dynamic
                        "market": "ETH-USD",  # make it dynamic
                        "side": "SELL",
                        "order_type": "MARKET",
                        "post_only": "false",
                        "size": size,  # make it dynamic
                        "price": market_price,  # make it dynamic
                        "limit_fee": "0.4",
                        "expiration_epoch_seconds": time.time() + SEVEN_DAYS_S + 60,
                        "time_in_force": "GTT",
                        "trailing_percent": "12",
                        "trigger_price": "1740",
                    }
                )
                dydx_order_details = vars(order_information)
                dydx_order_details = dydx_order_details["data"]["order"]
                order_manager.store_data(dydx_order_details, "dydx_orders")
                order_id = dydx_order_details["id"]
                print("order data", dydx_order_details)
                open_position = True
            except Exception as e:
                print(vars(e))


@app.task(name="cancel_order", default_retry_delay=4 * 60)
def cancel_order():
    trigger_price = 2000
    global order_id
    print(order_id)
    global open_position
    if open_position is True:
        load_contract = LoadContracts()
        market_price = load_contract.get_asset_price(
            "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
        )  # make it dynamic
        print(market_price)
        if trigger_price < market_price:
            try:
                order_manager = OrderManager()
                dydx_order = DydxOrder()
                cancelled_order_details = dydx_order.cancel_order(order_id)
                cancelled_order_details = vars(cancelled_order_details)
                cancelled_order_details = cancelled_order_details["data"]["cancelOrder"]
                order_manager.update_data(order_id, "dydx_orders", "CANCEL")
                print(cancelled_order_details)
                open_position = False
            except Exception as e:
                print(vars(e))
