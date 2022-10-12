
from components import FirebaseDataManager
from services.market_data.coingecko import CoinGecko


class PriceFloorManager:

    def set_price_floor(self, asset_name, number_of_days=30):
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
                "price_floor": asset_peak_price,
            }
            firebase_data_manager_obj.store_data(data, data["id"], "price_floor_data")
            return asset_peak_price
        except Exception as e:
            raise Exception(e)

    def get_price_floor(self, asset_name):
        firebase_data_manager_obj = FirebaseDataManager()

        asset_price_floor_details = firebase_data_manager_obj.fetch_data(
            asset_name, "price_floor_data"
        )
        asset_price_floor_details = asset_price_floor_details.to_dict()
        return asset_price_floor_details["price_floor"]



if __name__ == "__main__":
    a = PriceFloorManager()
    print(a.set_price_floor("ethereum"))
