from components import FirebaseDataManager
from services.market_data.coingecko import CoinGecko

firebase_data_manager_obj = FirebaseDataManager()


class PriceFloorManager:
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
            current_price_floor = asset_peak_price * 0.60
            # TODO: if  perivous_price_floor < current_price_floor : update the price floor, else don't update
            # get price floor
            firebase_data_manager_obj.store_data(
                data={
                    "id": asset_name,
                    "price_floor": current_price_floor,
                },
                document=asset_name,
                collection_name="price_floor_data",
            )

        except Exception as e:
            raise Exception(e)

    def get_asset_price_floor(self, asset_name):
        asset_price_floor_details = firebase_data_manager_obj.fetch_data(
            document_name=asset_name, collection_name="price_floor_data"
        )
        asset_price_floor_details = asset_price_floor_details.get("price_floor")
        return asset_price_floor_details

    def get_assets_price_floors(self):
        asset_price_floor_details = firebase_data_manager_obj.fetch_collections(
            "price_floor_data"
        )

        price_floors = {}
        for price_floor_detail in asset_price_floor_details:
            price_floor_detail_dict = price_floor_detail.to_dict()
            price_floors[price_floor_detail_dict["id"]] = price_floor_detail_dict[
                "price_floor"
            ]
        return price_floors


if __name__ == "__main__":
    a = PriceFloorManager()
    print(a.set_price_floor("bitcoin"))
