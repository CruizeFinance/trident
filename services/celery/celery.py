import json

from decouple import config
from web3 import Web3

from components import OrderManager
from services import DydxWithdrawal
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

@app.task(name="borrow_from_Aave", default_retry_delay=4 * 60)
def borrow_usdc_from_aave():
    global borrow_usdc
    if borrow_usdc is True:
        print("USDC already borrowed.")
        return

   # getting market price
    dydxabi = open("feed_abi.json")
    dydxabi_data = json.load(dydxabi)
    print(dydxabi_data)
    w3 = Web3(Web3.HTTPProvider(config("WEB_PROVIDER")))
    contract = w3.eth.contract(
            address=config("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"), abi=dydxabi_data
        )
    print(contract.functions)
    market_price = 1000
    floor_price = 1500
    x = 0.1
    trigger_price = 2000
    # call price feed  data api.
    # trigger_price = (floor_price * x) + floor_price
    if trigger_price >= market_price and borrow_usdc is False:

        #call the sc borrow usdc function.
        borrow_usdc = True
        print("USDC Borrow and Deposit in DYDX is Successful")

