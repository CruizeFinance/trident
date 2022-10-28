from decouple import config
from dydx3 import Client
from web3 import Web3

"""
This class DydxPClient is responsible for initializing the DydxClient instance.
It has a function __create_dydx_Instance() that is responsible for initializing the dydx instance and returning it.
"""


# TODO : make is singleton class


class DydxPClient(object):
    def create_dydx_instance(self, instance_data):
        api_credentials = instance_data["dydx_credentials"]["api_credentials"]
        wallet_credentials = instance_data["wallet_credentials"]
        client = Client(
            host=config("HOST"),
            network_id=config("NETWORK_ID"),
            stark_private_key=instance_data["dydx_credentials"]["stark_private_key"],
            web3=Web3(Web3.HTTPProvider(config("WEB_PROVIDER"))),
            eth_private_key=wallet_credentials["private_key"],
            api_key_credentials={
                "key": api_credentials["api_key"],
                "secret": api_credentials["secret_key"],
                "passphrase": api_credentials["passphrase"],
            },
        )
        return client


if __name__ == "__main__":
    d = DydxPClient()
