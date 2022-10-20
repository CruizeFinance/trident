"""
Class DydxAdmin  is used to manage  the dydx_user activity on dydx with APIS.
This class have some function that help the dydx_user to perform the activity on dydx.
"""


class DydxAdmin(object):

    """function createUser -  is used to create dydx_user on dydx
    @return crated dydx_user
    """

    def create_user(self, dydx_client):
        dydx_p_client = dydx_client["dydx_instance"]
        on_boarding_information = dydx_p_client.onboarding.create_user(
            # Optional if stark_private_key was provided.
            stark_public_key=dydx_client["stark_public_key"],
            stark_public_key_y_coordinate=dydx_client["stark_key_y_coordinate"],
            # Optional if eth_private_key or web3.eth.defaultAccount was provided.
            ethereum_address=dydx_client["default_address"],
            country="SG",
        )
        return on_boarding_information

    # function get_register_user is responsible register dydx_user on dydx.
    def register_user(self, dydx_client):
        dydx_p_client = dydx_client["dydx_instance"]
        signature = dydx_p_client.private.get_registration()
        if signature is None:
            return None
        return vars(signature)

    """function create_api is responsible for create api with dydx_user account on dydx
       @return created api.
    """

    def create_api_key(self, dydx_client):
        dydx_p_client = dydx_client["dydx_instance"]
        api_key_response = dydx_p_client.eth_private.create_api_key(
            ethereum_address=dydx_client["dydx_data"]["wallet_credentials"][
                "wallet_address"
            ],
        )
        return api_key_response

    """function get_api_keys is responsible for get api keys form dydx apis.
      @return dydx_user all apis
    """

    def get_api_keys(self, dydx_client):
        dydx_p_client = dydx_client["dydx_instance"]
        api_keys = dydx_p_client.private.get_api_keys()
        return api_keys

    def get_account(self, dydx_client):
        dydx_p_client = dydx_client["dydx_instance"]
        account_info = dydx_p_client.private.get_account(
            ethereum_address=dydx_client["dydx_data"]["wallet_credentials"][
                "wallet_address"
            ]
        )
        return account_info

    # return dydx_user dydx position_id.
    def get_position_id(self, dydx_client):
        user = self.get_account(dydx_client)
        user = vars(user)
        position_id = user["data"]["account"]["positionId"]
        return position_id


if __name__ == "__main__":
    a = DydxAdmin()
