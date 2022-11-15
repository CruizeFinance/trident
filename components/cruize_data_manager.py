from rest_framework.exceptions import ValidationError

from components import FirebaseDataManager
from utilities import cruize_constants


class CruizeDataManager(object):
    def save_asset_tvl(self, asset_data):
        firebase_db_manager_obj = FirebaseDataManager()
        asset_tvl_data = firebase_db_manager_obj.fetch_data(
            collection_name="assets_volume", document_name=asset_data["asset_name"]
        )
        tvl_data = {"name": None, "amount": None}
        if asset_tvl_data is not None:
            asset_tvl_amount = float(asset_tvl_data["amount"])
            asset_data["amount"] = float(asset_data["amount"])
            if asset_data["type"] == "protect":
                asset_tvl_amount += asset_data["amount"]

            else:
                asset_tvl_amount -= asset_data["amount"]
            tvl_data["name"] = asset_data["asset_name"]
            tvl_data["amount"] = asset_tvl_amount

        else:
            tvl_data["name"] = asset_data["asset_name"]
            tvl_data["amount"] = asset_data["amount"]

        firebase_db_manager_obj.store_data(
            collection_name="assets_volume",
            document=asset_data["asset_name"],
            data=tvl_data,
        )

    def fetch_user_transactions(self, user_data):
        firebase_db_obj = FirebaseDataManager()
        firebase_data = firebase_db_obj.fetch_sub_collections(
            cruize_constants.CRUIZE_USER, user_data["wallet_address"], "transactions"
        )
        if not firebase_data:
            return f"No data found for wallet address: {user_data['wallet_address']}"

        data = []
        if data is not None:
            for tnx_data in firebase_data:
                data.append(tnx_data.to_dict())
        return data


if __name__ == "__main__":
    d = CruizeDataManager()
    d.save_asset_tvl({"asset_name": "WBTC", "amount": "0.1", "type": "protect"})
