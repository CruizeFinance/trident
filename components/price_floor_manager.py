from datetime import datetime
from pytz import UTC
from dateutil.relativedelta import relativedelta

from components import FirebaseDataManager
from services.market_data.coingecko import CoinGecko


class PriceFloorManager:
    def get_price_floor(self, asset_name, number_of_days=30):
        today = datetime.today()
        price_floor_utc_time = today + relativedelta(months=1, day=1)
        price_floor_utc_time = price_floor_utc_time.replace(tzinfo=UTC)
        firebase_data_manager_obj = FirebaseDataManager()

        coin_gecko = CoinGecko()
        try:
            asset_price_data = coin_gecko.market_chart_day(
                asset_name, "usd", number_of_days
            )
            prices = []
            for i in range(0, len(asset_price_data["prices"])):
                prices.append(asset_price_data["prices"][i][1])
            prices.sort(reverse=True)
            asset_peak_price = prices[0]
            asset_peak_price = asset_peak_price * 0.85
            data = {
                "id": asset_name,
                "price_floor_utc_time": price_floor_utc_time,
                "price_floor": asset_peak_price,
            }
            firebase_data_manager_obj.store_data(data, data["id"], "price_floor_data")
            return asset_peak_price
        except Exception as e:
            raise Exception(e)

    def price_floor_details(self, asset_name, days):
        current_time_utc = datetime.today()

        current_time_utc = current_time_utc.replace(tzinfo=UTC)
        firebase_data_manager_obj = FirebaseDataManager()
        asset_price_floor_details = firebase_data_manager_obj.fetch_data(
            asset_name, "price_floor_data"
        )
        if asset_price_floor_details is not None:
            asset_price_floor_details = asset_price_floor_details.to_dict()
        try:
            if asset_price_floor_details is None:
                return self.get_price_floor(asset_name, days)
            price_floor_time_utc = asset_price_floor_details["price_floor_utc_time"]
            price_floor_time_utc = price_floor_time_utc.replace(tzinfo=UTC)
            if current_time_utc > price_floor_time_utc:
                return self.get_price_floor(asset_name, days)
            return asset_price_floor_details["price_floor"]
        except Exception as e:
            raise Exception(e)


if __name__ == "__main__":
    a = PriceFloorManager()
    a.get_price_floor("chainlink", 30)
