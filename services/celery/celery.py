from components import OrderManager
from services import DydxWithdrawal
from settings_config.celery import app


@app.task(name="check_withdrawal", default_retry_delay=4 * 60)
def check_withdrawal():
    dydx_withdrawal = DydxWithdrawal()
    order_manager = OrderManager()
    result = dydx_withdrawal.transfer({"limit": 100, "transfer_type": "WITHDRAWAL"})
    transfers = result["data"]["transfers"]
    for transfer in transfers:
        if transfer["status"] == "CONFIRMED":
            order_manager.update_on_firebase(transfer["id"], "withdrawal", "CONFIRMED")
