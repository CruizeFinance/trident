import json

from decouple import config
from web3 import Web3
from web3.middleware import geth_poa_middleware


class LoadContracts:
    def load_contracts(self, contract_address, contract_abi):
        contract_data = json.load(contract_abi)
        w3 = Web3(
            Web3.HTTPProvider(
                "https://mainnet.infura.io/v3/4e55b6d7c94d4c58a931971dc807d055"
            )
        )
        contract = w3.eth.contract(address=contract_address, abi=contract_data)
        return contract

    def web3_provider(self):
        web3 = Web3(Web3.HTTPProvider(config("WEB_PROVIDER")))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return web3

    def get_asset_price(self, asset_address):
        contract_abi = open("services/contracts/contract_abis/feed_abi.json")
        contract = self.load_contracts(asset_address, contract_abi)
        market_price = contract.functions.latestRoundData().call()
        market_price = market_price[1]
        market_price = market_price / 1e8
        return market_price
