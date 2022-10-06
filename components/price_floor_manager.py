from datetime import  datetime

from dateutil.relativedelta import relativedelta

from components import FirebaseDataManager
from services.market_data.coingecko import CoinGecko


class PriceFloorManager():
    def calculate_price_floor(self,asset_name, number_of_days=30):
        today = datetime.today()
        price_floor_time = today + relativedelta(months=1, day=1)
        firebase_data_manager_obj = FirebaseDataManager()

        coinGecko = CoinGecko()
        try:
            asset_price_data = coinGecko.market_chart_day(asset_name, 'usd', number_of_days)
            prices = []
            for i in range(0, len(asset_price_data['prices']) - 1):
                prices.append(asset_price_data['prices'][i][1])
            prices.sort(reverse=True)
            asset_peak_price = prices[0]
            asset_peak_price = asset_peak_price * 0.85
            data = {"id": asset_name, "price_floor_time": price_floor_time, 'price_floor': asset_peak_price}
            firebase_data_manager_obj.store_positions_data(data, 'Position_data')
            return asset_peak_price
        except Exception as e:
            raise Exception(e)

if __name__ == '__main__':
    a =  PriceFloorManager()
    a.calculate_price_floor('chainlink',30)