from services.dydx_client.dydx_p_client import DydxPClient
from decouple import config

"""
Class DydxAdmin  is used to manage  the user activity on dydx with APIS.
This class have some function that help the user to perform the activity on dydx.
"""


class DydxAdmin:
    Client = None

    def __init__(self):
        self.Client = DydxPClient()
        self.Client = self.Client.get_dydx_instance

    """ function createUser -  is used to create user on dydx
        @return crated user
    """

    def create_user(self):
        onboarding_information = self.Client.onboarding.create_user(
            # Optional if stark_private_key was provided.
            stark_public_key=config("STARK_PUBLIC_KEY"),
            stark_public_key_y_coordinate=config("STARK_KEY_Y_COORDINATE"),
            # Optional if eth_private_key or web3.eth.defaultAccount was provided.
            ethereum_address=config("ETH_ADDRESS"),
            country="SG",
        )
        return onboarding_information

    # function get_register_user is responsible register user on dydx.
    def register_user(self):
        signature = self.Client.private.get_registration()
        return signature

    """function create_api is responsible for create api with user account on dydx
       @return created api.
    """

    def create_api_key(self):
        api_key_response = self.Client.eth_private.create_api_key(
            ethereum_address=config("ETH_ADDRESS"),
        )
        return api_key_response

    """function get_api_keys is responsible for get api keys form dydx apis.
      @return user all apis
    """

    def get_api_keys(self):
        api_keys = self.Client.private.get_api_keys()
        return api_keys

    # return user .
    def get_account(self):
        account_info = self.Client.private.get_account(
            ethereum_address=config("ETH_ADDRESS"),
        )
        return account_info

    # return user dydx position_id.
    def get_position_id(self):
        user = self.get_account()
        user = vars(user)
        position_id = user["data"]["account"]["positionId"]
        return position_id
