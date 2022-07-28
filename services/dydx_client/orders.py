from services.dydx_client.dydx_p_client import DydxPClient

"""
This class is used  to manage The order's on dydx .
This class have   functions create_order() and cancel_orders() that are used to open and close position on dydx.
"""


class DydxOrder:
    CLIENT = None

    def __init__(self):
        self.CLIENT = DydxPClient()
        self.CLIENT = self.CLIENT.get_dydx_instance

    """ function is responsible for creating Order on dydx.
        @param order_params are order parameters that pass to dydx API.
         @return created Order information.   
    """

    def create_order(self, order_params):
        placed_order = self.CLIENT.private.create_order(
            position_id=order_params[
                "position_id"
            ],  # required for creating the order signature
            market=order_params["market"],
            side=order_params["side"],
            order_type=order_params["order_type"],
            post_only=order_params["post_only"],
            size=str(order_params["size"]),
            price=str(order_params["price"]),
            limit_fee=str(order_params["limit_fee"]),
            expiration_epoch_seconds=order_params["expiration_epoch_seconds"],
            time_in_force=order_params["time_in_force"],
        )
        return placed_order

    """ function is responsible for deleting the order on dydx.
        @param orderId orderId to be deleted.
        @return deleted order information.
    """

    def cancel_order(self, id):
        deleted_order = self.CLIENT.private.cancel_order(order_id=id)
        return deleted_order

    """ function get_market_orders is responsible for getting all the market order according to the order_params.
        @param Order_params are the parameters that pass to dydx3  API.
        @return Orders information.
    """

    def get_market_orders(self, order_params):
        all_orders = self.CLIENT.private.get_orders(
            market=order_params["market"],
            status=order_params["status"],
            side=order_params["side"],
            limit=order_params["limit"],
        )
        return all_orders
