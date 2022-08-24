from services.dydx_client.dydx_p_client import DydxPClient
from decouple import config

"""
Class DydxAdmin  is used to manage  the dydx_user activity on dydx with APIS.
This class have some function that help the dydx_user to perform the activity on dydx.
"""


class DydxAdmin(object):
    def __init__(self):
        self.client = DydxPClient()
        self.client = self.client.get_dydx_instance

    """ function createUser -  is used to create dydx_user on dydx
        @return crated dydx_user
    """

    def create_user(self):
        onboarding_information = self.client.onboarding.create_user(
            # Optional if stark_private_key was provided.
            stark_public_key=config("STARK_PUBLIC_KEY"),
            stark_public_key_y_coordinate=config("STARK_KEY_Y_COORDINATE"),
            # Optional if eth_private_key or web3.eth.defaultAccount was provided.
            ethereum_address=config("ETH_ADDRESS"),
            country="SG",
        )
        return onboarding_information

    # function get_register_user is responsible register dydx_user on dydx.
    def register_user(self):
        signature = self.client.private.get_registration()
        if(not signature is None):
           return vars(signature)
        return "user not get register"


    """function create_api is responsible for create api with dydx_user account on dydx
       @return created api.
    """

    def create_api_key(self):
        api_key_response = self.client.eth_private.create_api_key(
            ethereum_address=config("ETH_ADDRESS"),
        )
        return api_key_response

    """function get_api_keys is responsible for get api keys form dydx apis.
      @return dydx_user all apis
    """

    def get_api_keys(self):
        api_keys = self.client.private.get_api_keys()
        return api_keys

    # return dydx_user.
    def get_account(self):
        account_info = self.client.private.get_account(
            ethereum_address=config("ETH_ADDRESS"),
        )


        return account_info

    # return dydx_user dydx position_id.
    def get_position_id(self):
        user = self.get_account()
        user = vars(user)
        position_id = user["data"]["account"]["positionId"]
        return position_id


