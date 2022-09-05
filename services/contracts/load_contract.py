import json

from decouple import config
from web3 import Web3


class LoadContracts():

    def load_contracts(self,contract_address,contract_abi):
        contract_data = json.load(contract_abi)
        w3 = self.web3_provider()
        contract = w3.eth.contract(
            address=contract_address, abi=contract_data
        )
        return contract

    def web3_provider(self):
       return  Web3(Web3.HTTPProvider(config("WEB_PROVIDER")))

    def get_asset_price(self,asset_address,abi):
        contract = self.load_contracts(asset_address, abi)
        market_price = contract.functions.latestRoundData().call()
        market_price = market_price[1]
        market_price = market_price / 1e8
        return market_price
