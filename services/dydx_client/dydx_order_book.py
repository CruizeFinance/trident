
from services import DydxPClient

"""
This class DydxPClient is responsible for initializing the DydxClient instance.
It has a function __create_dydx_Instance() that is responsible for initializing the dydx instance and returning it.
"""


class DydxOrderBook(object):

    def __init__(self):
        self.dydx_instance = DydxPClient()
        self.dydx_instance = self.dydx_instance.get_dydx_instance

    def get_order_book(self, market="ETH-USD"):

        order_book =  self.dydx_instance.public.get_orderbook(
            market=market,
        )
        return order_book.data



if __name__ == "__main__":
    d = DydxOrderBook()

    d = d.get_order_book(market="BTC-USD")
    print(d['asks'][0])
    print(d['bids'][0])
