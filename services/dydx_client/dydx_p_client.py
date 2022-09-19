from decouple import config
from dydx3 import Client
from web3 import Web3

"""
This class DydxPClient is responsible for initializing the DydxClient instance.
It has a function __create_dydx_Instance() that is responsible for initializing the dydx instance and returning it.
"""


# TODO : make is singleton class


class DydxPClient(object):
    def __init__(self):
        self.client = None

    def create_dydx_Instance(self):
        self.client = Client(
            host=config("HOST"),
            network_id=config("NETWORK_ID"),
            stark_private_key=config("STARK_PRIVATE_KEY"),
            web3=Web3(Web3.HTTPProvider(config("WEB_PROVIDER"))),
            api_key_credentials={
                "key": config("API_KEY"),
                "secret": config("SECRET_KEY"),
                "passphrase": config("PASSPHRASE"),
            },
        )

        return self.client

    @property
    def get_dydx_instance(self):
        if self.client is not None:
            return self.client
        return self.create_dydx_Instance()


if __name__ == "__main__":
    d = DydxPClient()
    print(vars(d.get_dydx_instance))
