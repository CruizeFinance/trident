
import time

from dydx3 import constants, epoch_seconds_to_iso

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

        withdrawal_amount = withdrawal_params['withdrawalamount']
        fast_withdrawal_result = self.get_transfer(withdrawal_amount)
        lp_position_id_result = list(fast_withdrawal_result.data['liquidityProviders'].keys())[0]
        quote = fast_withdrawal_result.data['liquidityProviders'][lp_position_id_result]['quote']
        if quote is None:
            raise Exception("Could not get a quote")
        debit_amount = quote['debitAmount']
        create_fast_withdrawal_result = self.client.private.create_fast_withdrawal(
            position_id=withdrawal_params['position_id'],
            credit_asset=constants.ASSET_USDC,
            credit_amount=withdrawal_amount,
            debit_amount=debit_amount,
            to_address=withdrawal_params['to_address'],
            lp_position_id=lp_position_id_result,
            lp_stark_public_key=list(fast_withdrawal_result.data['liquidityProviders'].values())[0]['starkKey'],
            expiration=epoch_seconds_to_iso(time.time() + 604801)
        )
        return create_fast_withdrawal_result.data


    def transfer(self, params):
        transfers = self.client.private.get_transfers(**params)
        return vars(transfers)


    def get_transfer(self, withdrawalamount):
        get_fast_withdrawal_result = self.client.public.get_fast_withdrawal(
            creditAsset=constants.ASSET_USDC,
            creditAmount=withdrawalamount
        )
        return get_fast_withdrawal_result


