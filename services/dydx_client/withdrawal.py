from services.dydx_client.dydx_p_client import DydxPClient

"""
This class is used  to manage The order's on dydx .
This class have   functions create_order() and cancel_orders() that are used to open and close position on dydx.
"""
<<<<<<< HEAD


class DydxWithdrawal:
    def __init__(self):
        self.client = DydxPClient()
        self.client = self.client.get_dydx_instance
=======
class DydxWithdrawal:
    CLIENT = None

    def __init__(self):
        self.CLIENT = DydxPClient()
        self.CLIENT = self.CLIENT.get_dydx_instance
>>>>>>> 393c1c8 (wrote withdrawal api for dydx and test it on mainnet)

    """ function is responsible for withdrawing USDC from dydx.
        @param order_params are order parameters that pass to dydx API.
         @return withdrawal information.   
    """

    def slow_withdrawal(self, withdrawal_params):
<<<<<<< HEAD
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
=======
        withdrawal = self.CLIENT.private.create_withdrawal(**withdrawal_params)
        return vars(withdrawal)

    def fast_withdrawal(self, withdrawal_params):
        fast_withdrawal = self.CLIENT.private.create_fast_withdrawal(
>>>>>>> 393c1c8 (wrote withdrawal api for dydx and test it on mainnet)
            **withdrawal_params
        )
        return vars(fast_withdrawal)

<<<<<<< HEAD
    def transfer(self, params):
        transfers = self.client.private.get_transfers(**params)
        return vars(transfers)
=======
    def get_transfer_info(self, params):
        transfers = self.CLIENT.private.get_transfers(**params)
        return vars(transfers)
>>>>>>> 393c1c8 (wrote withdrawal api for dydx and test it on mainnet)
