from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from utilities.enums import AssetCodes


class AaveApy(object):
    def __init__(self):
        self.aave_sub_graph_url = (
            "https://api.thegraph.com/subgraphs/name/aave/protocol-v2"
        )
        self.avve_sub_graph_query = """
                query {
                  reserves (where: {
                    usageAsCollateralEnabled: true
                  }) {
                    id
                    name
                    price {
                      id
                      priceInEth
                    }
                    liquidityRate
                    variableBorrowRate
                    stableBorrowRate
                    aEmissionPerSecond
                    vEmissionPerSecond
                    decimals
                    totalATokenSupply
                    totalCurrentVariableDebt
                    symbol
                  }
                }
                """
        self.aave_ray = 10.0**27
        self.aave_asset_symbols = {"bitcoin": "WBTC", "ethereum": "WETH"}

    def fetch_asset_apys(self):
        query = gql(self.avve_sub_graph_query)
        transport = RequestsHTTPTransport(
            url=self.aave_sub_graph_url,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport)

        response = client.execute(query)
        apy_graph_data = response["reserves"]
        subset_of_apy_asset = set(self.aave_asset_symbols.values())
        apy_data = [i for i in apy_graph_data if i["symbol"] in subset_of_apy_asset]
        asset_apy = {}

        for interval in range(len(apy_data)):
            token_liquidityRate = int(apy_data[interval]["liquidityRate"]) * 100
            asset_apy[AssetCodes.asset_name.value[apy_data[interval]["symbol"]]] = (
                token_liquidityRate / self.aave_ray
            )

        return asset_apy

    def store_asset_apys(self, asset_apys=None):
        from components import FirebaseDataManager

        firebase_data_manager_obj = FirebaseDataManager()

        if not asset_apys:
            asset_apys = self.fetch_asset_apys()
        firebase_data_manager_obj.bulk_store(
            data=asset_apys, collection_name="asset_apys", field="apy"
        )


if __name__ == "__main__":
    a = AaveApy()
    print(a.store_asset_apys())
