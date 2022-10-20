import time
from binance.client import Client as Client_binance
from settings_config import dydx_instances


class BinanceClient(object):
    def __init__(self):
        # TODO: need to store some where secure.
        dydx_instances_details = dydx_instances["BTC-USD"]["binance_credentials"]
        self.binance_api_key = dydx_instances_details["binance_api_key"]
        self.binance_api_secret = dydx_instances_details["binance_api_secret"]
        self.client = Client_binance(
            api_key=self.binance_api_key, api_secret=self.binance_api_secret
        )

    def price_data_per_interval(self, symbol, start_time, end_time):
        data = self.client.get_historical_klines(
            symbol=symbol,
            interval=self.client.KLINE_INTERVAL_1MINUTE,
            end_str=end_time,
            start_str=start_time,
        )
        prices = []
        for interval in range(0, len(data)):
            prices.append(data[interval][4])

        return prices


if __name__ == "__main__":
    a = BinanceClient()
    # start <= endtime
    print(time.time())
    print(a.price_data_per_interval("ETHBUSD", str(1665543038000), str(1665546038378)))
    print(time.time())
