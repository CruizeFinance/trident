from dydx3.constants import (
    ASSET_USDC,
    ACCOUNT_ACTION_WITHDRAWAL,
    ACCOUNT_ACTION_DEPOSIT,
)

from services.dydx_client.dydx_p_client import DydxPClient

"""
This class is used  to manage The order's on dydx .
This class have   functions create_order() and cancel_orders() that are used to open and close position on dydx.
"""


class DydxWithdrawal:
    CLIENT = None

    def __init__(self):
        self.CLIENT = DydxPClient()
        self.CLIENT = self.CLIENT.get_dydx_instance

    """ function is responsible for withdrawing USDC from dydx.
        @param order_params are order parameters that pass to dydx API.
         @return withdrawal information.   
    """

    def slow_withdrawal(self, withdrawal_params):
        withdrawal = self.CLIENT.private.create_withdrawal(**withdrawal_params)
        return vars(withdrawal)

    def fast_withdrawal(self, withdrawal_params):
        fast_withdrawal = self.CLIENT.private.create_fast_withdrawal(
            **withdrawal_params
        )
        return vars(fast_withdrawal)

    def get_transfer_info(self, params):
        transfers = self.CLIENT.private.get_transfers(**params)
        return vars(transfers)
