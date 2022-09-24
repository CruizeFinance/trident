from services import LoadContracts
from utilities import cruize_constants


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
