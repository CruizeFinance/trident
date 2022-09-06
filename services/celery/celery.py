import json

from decouple import config
from web3 import Web3

from components import OrderManager
from services import DydxWithdrawal, LoadContracts

from settings_config.celery import app

borrow_usdc = False
deposit_to_dydx = False




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


@app.task(name="borrow_from_aave", track_started=True)
def borrow_usdc_from_aave():
    global borrow_usdc
    print(borrow_usdc)
    if borrow_usdc is True:
        print("USDC already borrowed.")
    # getting market price
    load_contract = LoadContracts()
    contract_abi = open("services/celery/feed_abi.json")
    market_price = load_contract.get_asset_price('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419', contract_abi)
    print(market_price)
    floor_price = 1500
    x = 0.1
    # call price feed  data api.
    trigger_price = (floor_price * x) + floor_price
    if trigger_price >= market_price and borrow_usdc is False:
        # call the sc borrow usdc function.
        borrow_usdc = True
        print("USDC Borrow and Deposit in DYDX is Successful")


# @app.task(name="deposit_to_gnosis", default_retry_delay=4 * 60)
# def deposit_to_gnosis():
#     global deposit_to_dydx
#     if deposit_to_dydx is False and borrow_usdc is True:
#         # transfer fund to gnosis
#         deposit_to_dydx = True
app.conf.beat_schedule = {
    "borrow_from_aave": {
        "task": "celery.borrow_usdc_from_aave",
        "schedule": 10.0
    }
}