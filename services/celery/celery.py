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


app.conf.beat_schedule = {
    "borrow_from_aave": {"task": "celery.borrow_usdc_from_aave", "schedule": 10.0}
}
