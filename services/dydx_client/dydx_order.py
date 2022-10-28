from services.dydx_client.dydx_p_client import DydxPClient

"""
This class is used  to manage The order's on dydx .
This class have   functions create_order() and cancel_orders() that are used to open and close position on dydx.
"""


class DydxOrder:

    """
    function is responsible for creating Order on dydx.
    @param order_params are order parameters that pass to dydx API.
    @return created Order information.
    """

    def create_order(self, order_params, dydx_client):
        dydx_p_client = dydx_client["dydx_instance"]
        placed_order_details = dydx_p_client.private.create_order(**order_params)
        return placed_order_details

    """ function is responsible for deleting the order on dydx.
        @param orderId orderId to be deleted.
        @return deleted order information.
    """

    def cancel_order(self, id, dydx_client):
        deleted_order = dydx_client.private.cancel_order(order_id=id)
        return deleted_order

    """ function get_market_orders is responsible for getting all the market order according to the order_params.
        @param Order_params are the parameters that pass to dydx3  API.
        @return Orders information.
    """

    def get_market_orders(self, order_params, dydx_client):
        all_orders = dydx_client.private.get_orders(
            market=order_params["market"],
            status=order_params["status"],
            side=order_params["side"],
            limit=order_params["limit"],
        )
        return all_orders

    def get_order_book(self, dydx_client, market="ETH-USD"):
        dydx_p_client = dydx_client["dydx_instance"]
        order_book = dydx_p_client.public.get_orderbook(
            market=market,
        )
        if order_book is not None:
            order_book = vars(order_book)
        return order_book["data"]
