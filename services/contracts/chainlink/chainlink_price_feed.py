import json
from web3 import Web3

from services import LoadContracts
from utilities import cruize_constants
from utilities.cruize_constants import MAINNET_INFURA_URL


class ChainlinkPriceFeed:
    def __init__(self):
        self.load_contract = LoadContracts()

    def get_asset_price(self, asset_address):
        contract_abi = open("services/contracts/chainlink/chainlink_price_feed.json")
        contract = self.load_contract.load_contracts(asset_address, contract_abi)
        market_price = contract.functions.latestRoundData().call()
        market_price = market_price[1]
        market_price = market_price / cruize_constants.DECIMAL_NOTATION
        return market_price

    def get_asset_price_mainnet(self, asset_address):
        web3 = Web3(Web3.HTTPProvider(MAINNET_INFURA_URL))
        contract_abi = open("services/contracts/chainlink/chainlink_price_feed.json")
        contract_data = json.load(contract_abi)
        contract = web3.eth.contract(address=asset_address, abi=contract_data)
        market_price = contract.functions.latestRoundData().call()
        market_price = market_price[1]
        market_price = market_price / cruize_constants.DECIMAL_NOTATION
        return market_price
    """
      :method - get_oracle_market_price.
      :params   - asset_oracle_address:oracle address of asset.
      :return   - asset market price. 
    """

    def get_oracle_market_price(self, asset_oracle_address):
        market_price = self.get_asset_price(
            asset_oracle_address
        )
        return market_price