from components import OrderManager
from services import DydxWithdrawal, LoadContracts

from settings_config.celery_config import app

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
    if borrow_usdc is True:
        print("USDC already borrowed.")
    # getting market price
    load_contract = LoadContracts()
    contract_abi = open("services/contracts/contract_abis/feed_abi.json")
    market_price = load_contract.get_asset_price(
        "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", contract_abi
    )
    floor_price = 1500
    x = 0.1
    # call price feed  data api.
    # trigger_price = (floor_price * x) + floor_price
    trigger_price = 1700
    if trigger_price >= market_price and borrow_usdc is False:
        # call the sc borrow usdc function.
        borrow_usdc = True
        print("USDC Borrow and Deposit in DYDX is Successful")


@app.task(name="deposit_to_gnosis", default_retry_delay=4 * 60)
def deposit_to_gnosis():
    global deposit_to_dydx
    if deposit_to_dydx is False and borrow_usdc is True:
        load_contract = LoadContracts()
        cruize_contract = load_contract.load_contracts(
            0x5F4EC3DF9CBD43714FE2740F5E3616155C5B8419, contract_abi
        )
        # transfer fund to gnosis
        deposit_to_dydx = True


# deposit to gnosis
# deposit to aave from gnosis
# take lone from avve
