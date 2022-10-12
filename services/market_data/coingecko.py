import requests
from datetime import datetime
from services.contracts.chainlink import ChainlinkPriceFeed
from utilities import cruize_constants

# class -  coinGecko:  is responsible for returning market data.
from utilities.datetime_utilities import convert_epoch_to_utcdatetime


class CoinGecko:

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
        try:
            result = dict(requests.get(url).json())
            error = result.get("status", "Not found")
            if error == "Not found":
                for key, value in result.items():
                    for i, data in enumerate(result[key]):
                        result[key][i][0] = convert_epoch_to_utcdatetime(
                            int(result[key][i][0]) / 1000, parser="%m-%d/%H:%M"
                        )
                        result[key][i][1] = round(int(result[key][i][1]), 3)
                return result
            result = result.get("status")
            raise Exception(result["error_message"])
        except Exception as e:
            raise Exception(e)

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
        error = result.get("status", "Not found")
        if error == "Not found":
            for key, value in result.items():
                for i, data in enumerate(result[key]):
                    result[key][i][0] = convert_epoch_to_utcdatetime(
                        int(result[key][i][0]) / 1000, parser="%m-%d/%H:%M"
                    )
                    result[key][i][1] = round(int(result[key][i][1]), 3)

            return result
        result = result.get("status")
        raise Exception(result["error_message"])

    def asset_price(self, asset_address):
        chainlink_price_feed = ChainlinkPriceFeed()
        market_price = chainlink_price_feed.get_asset_price_mainnet(
            asset_address["asset_address"]
        )
        return market_price
