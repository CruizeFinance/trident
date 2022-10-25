from components import FirebaseDataManager
from services.market_data.coingecko import CoinGecko


class PriceFloorManager:
    def __init__(self):
        self.firebase_data_manager_obj = FirebaseDataManager()

    def set_price_floor(self, asset_name, number_of_days=30):

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
            self.firebase_data_manager_obj.store_data(
                data=data, id=data["id"], collection_name="price_floor_data"
            )
            return asset_peak_price
        except Exception as e:
            raise Exception(e)

    def get_price_floor(self, asset_name):
        asset_price_floor_details = self.firebase_data_manager_obj.fetch_data(
            document_name=asset_name, collection_name="price_floor_data"
        )
        asset_price_floor_details = asset_price_floor_details
        asset_price_floor_details = asset_price_floor_details.get("price_floor")
        return asset_price_floor_details

    def assets_price_floor(self):
        asset_price_floor_details = self.firebase_data_manager_obj.fetch_collections()
        return asset_price_floor_details


if __name__ == "__main__":
    a = PriceFloorManager()
    print(a.set_price_floor("bitcoin"))
