import requests
from datetime import datetime

from utilities import datetime_utilities

HOST = "https://api.coingecko.com/api/v3"
SECONDS_PER_HOUR = 3600


def market_chart_day(asset="ethereum", vs_currency="usd", days=2):
    url = HOST + f"/coins/{asset}/market_chart?vs_currency={vs_currency}&days={days}"
    result = dict(requests.get(url).json())
    for key, value in result.items():
        for i, data in enumerate(result[key]):
            result[key][i][0] = datetime_utilities.convert_epoch_to_utcdatetime(
                int(result[key][i][0]) / 1000, parser="%m-%d/%H:%M"
            )
            result[key][i][1] = round(int(result[key][i][1]), 3)
    return result


def market_chart_timestamp(
    asset="ethereum",
    vs_currency="usd",
    time_from=datetime.utcnow().timestamp() - SECONDS_PER_HOUR,
    time_to=datetime.utcnow().timestamp(),
):
    url = (
        HOST
        + f"/coins/{asset}/market_chart/range?vs_currency={vs_currency}&from={time_from}&to={time_to}"
    )
    result = dict(requests.get(url).json())
    for key, value in result.items():
        for i, data in enumerate(result[key]):
            result[key][i][0] = datetime_utilities.convert_epoch_to_utcdatetime(
                int(result[key][i][0]) / 1000, parser="%m-%d/%H:%M"
            )
            result[key][i][1] = round(int(result[key][i][1]), 3)

    return result


def asset_price(asset="bitcoin", vs_currencies="usd"):
    url = HOST + f"/simple/price?ids={asset}&vs_currencies={vs_currencies}"
    result = dict(requests.get(url).json())
    return result[asset][vs_currencies]


if __name__ == "__main__":
    print(market_chart_day())
    # print(market_chart_timestamp())
    print(asset_price())
