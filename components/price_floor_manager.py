from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta

from components import FirebaseDataManager
from services.market_data.coingecko import CoinGecko


class PriceFloorManager:

    def get_gprice_floor(self,asset_name, number_of_days=30):
        today = datetime.today()
        price_floor_time = today + relativedelta(months=1, day=1)
        firebase_data_manager_obj = FirebaseDataManager()

        coin_gecko = CoinGecko()
        try:
            asset_price_data = coin_gecko.market_chart_day(
                asset_name, "usd", number_of_days
            )
            prices = []
            for i in range(0, len(asset_price_data["prices"]) - 1):
                prices.append(asset_price_data["prices"][i][1])
            prices.sort(reverse=True)
            asset_peak_price = prices[0]
            asset_peak_price = asset_peak_price * 0.85
            data = {
                "id": asset_name,
                "price_floor_time": price_floor_time,
                "price_floor": asset_peak_price,
            }
            firebase_data_manager_obj.store_data(data,data['id'] ,"Position_data")
            return asset_peak_price
        except Exception as e:
            raise Exception(e)

    def price_floor_details(self, asset_name, days):
        current_time = datetime.today()
        utc = pytz.UTC
        current_time = current_time.replace(tzinfo=utc)
        firebase_data_manager_obj = FirebaseDataManager()
        asset_price_floor_details = firebase_data_manager_obj.fetch_data(asset_name, "Position_data")
        if asset_price_floor_details is not None:
            asset_price_floor_details = asset_price_floor_details.to_dict()
        try:
            if asset_price_floor_details is None:
                return self.get_price_floor(asset_name, days)
            price_floor_date = asset_price_floor_details["price_floor_time"]
            price_floor_date = price_floor_date.replace(tzinfo=utc)
            if current_time > price_floor_date:
                return self.get_price_floor(asset_name, days)
            return asset_price_floor_details["price_floor"]
        except Exception as e:
            raise Exception(e)


if __name__ == "__main__":
    a = PriceFloorManager()
    a.get_price_floor("chainlink", 30)
