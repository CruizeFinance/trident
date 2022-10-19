import time
from dydx3 import constants, epoch_seconds_to_iso
from tests.constants import SEVEN_DAYS_S

from services.dydx_client.dydx_p_client import DydxPClient

# class  - DydxWithdrawal: is used to manage withdrawal on dydx .


class DydxWithdrawal:
    def __init__(self):
        self.client = DydxPClient()
        self.client = self.client.get_dydx_instance

    """    
           :method  -   slow_withdrawal: responsible for withdrawing USDC from dydx . this send an request to dydx contract to withdraw usdc.
           :param   -   withdrawal_params are  parameters that pass to dydx API.
           :return  -   withdrawal information.   
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

    """ 
        :method -   fast_withdrawal: responsible for withdrawing USDC from dydx.this send an request to dydx pool to withdraw usdc that is of chain.
        :param   -   withdrawal_params are  parameters that pass to dydx API.
        :return  -   withdrawal information.   
    """

    def fast_withdrawal(self, withdrawal_params):
        withdrawal_amount = withdrawal_params["withdrawal_amount"]
        fast_withdrawal_result = self.fast_withdrawal_details(withdrawal_amount)
        lp_position_id_result = list(
            fast_withdrawal_result.data["liquidityProviders"].keys()
        )[0]
        quote = fast_withdrawal_result.data["liquidityProviders"][
            lp_position_id_result
        ]["quote"]
        if quote is None:
            raise Exception("Could not get a quote")
        debit_amount = quote["debitAmount"]
        create_fast_withdrawal_result = self.client.private.create_fast_withdrawal(
            position_id=withdrawal_params["position_id"],
            credit_asset=constants.ASSET_USDC,
            credit_amount=withdrawal_amount,
            debit_amount=debit_amount,
            to_address=withdrawal_params["to_address"],
            lp_position_id=lp_position_id_result,
            lp_stark_public_key=list(
                fast_withdrawal_result.fetch_collections["liquidityProviders"].values()
            )[0]["starkKey"],
            expiration=epoch_seconds_to_iso(time.time() + SEVEN_DAYS_S),
        )
        return create_fast_withdrawal_result.data

    """ 
        :method -   all_transfer_details: responsible return all the transfer that has been   initiated.
        :return  -   all transfer details .   
    """

    def all_transfer_details(self, params):
        transfers = self.client.private.get_transfers(**params)
        return vars(transfers)

    """ 
         :method -   fast_withdrawal_details: responsible return all the fast withdrawal details that has been initiated.
         :return  -   all transfer details .   
     """

    def fast_withdrawal_details(self, withdrawal_amount):
        get_fast_withdrawal_result = self.client.public.get_fast_withdrawal(
            creditAsset=constants.ASSET_USDC, creditAmount=withdrawal_amount
        )
        return get_fast_withdrawal_result
