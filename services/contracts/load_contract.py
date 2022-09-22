import json

from decouple import config
from web3 import Web3
from web3.middleware import geth_poa_middleware


class LoadContracts:
    def load_contracts(self, contract_address, contract_abi):
        contract_data = json.load(contract_abi)
        w3 = self.web3_provider()

        contract = w3.eth.contract(address=contract_address, abi=contract_data)
        return contract

    def web3_provider(self):
        web3 = Web3(Web3.HTTPProvider(config("WEB_PROVIDER")))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return web3
