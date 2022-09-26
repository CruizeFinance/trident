import requests
from datetime import datetime

from services.contracts.chainlink import ChainlinkPriceFeed
from utilities import cruize_constants
from utilities.utills import Utilities


# class -  coinGecko:  is responsible for returning market data.

class CoinGecko:
    def __init__(self):
        self.utilities = Utilities()

    """
      :method   - market_chart_day: will return daily market price data for each one hour.
      :params   - asset:asset for which market price data will fetch.
      :params   - vs_currency:such as ETH-USD.
      :params   - days: for how much days data is need.
      :return   - asset market price. 
    """
    def market_chart_day(self, asset="ethereum", vs_currency="usd", days=2):
        url = (
                cruize_constants.COINGECKO_HOST
                + f"/coins/{asset}/market_chart?vs_currency={vs_currency}&days={days}"
        )

        result = dict(requests.get(url).json())
        error = result.get("error", "Not found")
        if error is "Not found":
            self.utilities.formate_price_data(result)
            return result
        raise Exception(result['error'])
    """
      :method   - market_chart_timestamp: will return market price data with timestamp like 1 day , 1 hour e,1 month etc.
      :params   - asset:asset for which market price data will fetch.
      :params   - vs_currency:such as ETH-USD.
      :return   - asset market price. 
    """
    def market_chart_timestamp(
            self,
            asset="ethereum",
            vs_currency="usd",
            time_from=datetime.utcnow().timestamp() - cruize_constants.SECONDS_PER_HOUR,
            time_to=datetime.utcnow().timestamp(),
    ):
        url = (
                cruize_constants.COINGECKO_HOST
                + f"/coins/{asset}/market_chart/range?vs_currency={vs_currency}&from={time_from}&to={time_to}"
        )
        result = dict(requests.get(url).json())
        error = result.get("error", "Not found")
        if error is "Not found":
            self.utilities.formate_price_data(result)
            return result
        raise Exception(result['error'])

    def asset_price(self, asset_address):
        chainlinkpricefeed =  ChainlinkPriceFeed()
        market_price = chainlinkpricefeed.get_asset_price(asset_address['asset_address'])
        return market_price


if __name__ == '__main__':
    a = CoinGecko()
    a.market_chart_day()
