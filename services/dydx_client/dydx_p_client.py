from decouple import config
from dydx3 import Client
from web3 import Web3


"""
This class DydxPClient is responsible for initializing the DydxClient instance.
It has a function __create_dydx_Instance() that is responsible for initializing the dydx instance and returning it.
"""


# TODO : make is singleton class
class DydxPClient:
    CLIENT = None

    def _create_dydx_Instance(self):
        self.CLIENT = Client(
            host=config("HOST"),
            network_id=config("NETWORK_ID"),
            eth_private_key=config("PRIVATE_KEY"),
            stark_private_key=config("STARK_PRIVATE_KEY"),
            web3=Web3(Web3.HTTPProvider(config("WEB_PROVIDER"))),
            api_key_credentials={
                "key": config("API_KEY"),
                "secret": config("SECRET_KEY"),
                "passphrase": config("PASSPHRASE"),
            },
        )
        return self.CLIENT

    @property
    def get_dydx_instance(self):
        if self.CLIENT != None:
            return self.CLIENT

        return self._create_dydx_Instance()
