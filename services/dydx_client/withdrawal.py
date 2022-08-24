from services.dydx_client.dydx_p_client import DydxPClient

"""
This class is used  to manage The order's on dydx .
This class have   functions create_order() and cancel_orders() that are used to open and close position on dydx.
"""


class DydxWithdrawal:
    def __init__(self):
        self.client = DydxPClient()
        self.client = self.client.get_dydx_instance

    """ function is responsible for withdrawing USDC from dydx.
        @param order_params are order parameters that pass to dydx API.
         @return withdrawal information.   
    """

    def slow_withdrawal(self, withdrawal_params):
        withdrawal = self.client.private.create_withdrawal(
            position_id=withdrawal_params["position_id"],
            amount=withdrawal_params["amount"],
            asset=withdrawal_params["asset"],
            expiration_epoch_seconds=withdrawal_params["expiration_epoch_seconds"],
            to_address=withdrawal_params["to_address"],
        )
        return vars(withdrawal)

    def fast_withdrawal(self, withdrawal_params):
        fast_withdrawal = self.client.private.create_fast_withdrawal(
            **withdrawal_params
        )
        return vars(fast_withdrawal)

    def transfer(self, params):
        transfers = self.client.private.get_transfers(**params)
        return vars(transfers)
