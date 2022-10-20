from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from utilities import cruize_constants
from utilities.enums import AssetCodes


class AaveApy:
    def fetch_asset_apys(self):
        query = gql(cruize_constants.AVVE_SUB_GRAPH_QUERY)
        transport = RequestsHTTPTransport(
            url=cruize_constants.AAVE_SUB_GRAPH_URL,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport)

        response = client.execute(query)
        apy_graph_data = response["reserves"]
        subset_of_apy_asset= set(cruize_constants.AAVE_APY_ASSET)
        apy_data = [i for i in apy_graph_data if i["symbol"] in subset_of_apy_asset]
        asset_apy = {}

        for interval in range(len(apy_data)):
            token_liquidityRate = int(apy_data[interval]["liquidityRate"]) * 100
            asset_apy[AssetCodes.asset_name.value[apy_data[interval]["symbol"]]] = (
                token_liquidityRate / cruize_constants.AAVE_RAY
            )

        return asset_apy


if __name__ == "__main__":
    a = AaveApy()
    print(a.fetch_asset_apys())
