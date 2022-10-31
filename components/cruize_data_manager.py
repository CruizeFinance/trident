from components import FirebaseDataManager


class CruizeDataManager(object):

    def save_TVL(self, asset_data):
        firebase_db_manager_obj = FirebaseDataManager()
        asset_tvl_data = firebase_db_manager_obj.fetch_data(collection_name="assets_volume",
                                                            document_name=asset_data['asset_name'])
        if asset_tvl_data is not None:
            asset_tvl_amount = float(asset_tvl_data['amount'])
            asset_data['amount'] = float(asset_data['amount'])
            if asset_data['type'] == 'protect':
                asset_tvl_amount += asset_data['amount']
            else:
                asset_tvl_amount -= asset_data['amount']
            tvl_data = {'name': None, 'amount': None}
            tvl_data['name'] = asset_data['asset_name']
            tvl_data['amount'] = asset_tvl_amount
            firebase_db_manager_obj.store_data(collection_name="assets_volume", document=asset_data['asset_name'],
                                               data=tvl_data)


if __name__ == '__main__':
    d = CruizeDataManager()
    d.save_TVL({'asset_name': 'WBTC', 'amount': '0.1', "type": 'protect'})
