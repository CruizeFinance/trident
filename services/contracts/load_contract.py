import json
from decouple import config
from web3 import Web3
from web3.middleware import geth_poa_middleware

# class -  LoadContracts: is responsible for lading contract and web3
class LoadContracts:

    """
    :method - load_contracts.
    :params - contract_address: address of contract to load.
    :params - contract_abi: abi of contract to load.
    :return - contract instance.
    """

    def load_contracts(self, contract_address, contract_abi):
        contract_data = json.load(contract_abi)
        w3 = self.web3_provider()

        contract = w3.eth.contract(address=contract_address, abi=contract_data)
        return contract

    """
      :method -  web3_provider:load web3 provider.
      :return - web3 instance. 
    """

    def web3_provider(self):
        web3 = Web3(Web3.HTTPProvider(config("WEB_PROVIDER")))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return web3
