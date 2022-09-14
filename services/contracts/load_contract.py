import json

from decouple import config
from web3 import Web3
from web3.middleware import geth_poa_middleware

from services import DydxAdmin


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

    def get_asset_price(self, asset_address):
        contract_abi = open("services/contracts/contract_abis/feed_abi.json")
        contract = self.load_contracts(asset_address, contract_abi)
        market_price = contract.functions.latestRoundData().call()
        market_price = market_price[1]
        market_price = market_price / 1e8
        return market_price

    def order_params(self):
        order_prams = {"position_id": None, "size": None, "market_price": None}
        market_price = self.get_asset_price(
            "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
        )  # make it dynamic
        admin = DydxAdmin()
        user = admin.get_account()
        user = vars(user)
        user_balance = user["data"]["account"]["equity"]
        position_id = user["data"]["account"]["positionId"]
        size = float(user_balance) / market_price
        size *= 5
        order_prams["size"] = str(round(size, 3))
        order_prams["position_id"] = position_id
        order_prams["market_price"] = market_price
        return order_prams
