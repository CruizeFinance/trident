from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from components import OrderManager
from order.serializers import (
    OrderRequestSerializer,
    CancelOrderRequestSerializer,
    FirestoreOrdersRequestSerializer,
)
from services import DydxOrder, DydxAdmin


class Order(GenericViewSet):
    """
    method create() is used to create order on dydx.
    :param - request will contain order details to place.
    this method will call the dydx_client method create_order with given params.
    :return order details that has been placed.
    """

    def create(self, request):
        self.serializer_class = OrderRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_data = serializer.data
        dydx_order = DydxOrder()
        order_manager = OrderManager()
        result = {"message": None, "error": None}

        try:
            dydx_order_details = dydx_order.create_order(order_data)
            dydx_order_details = vars(dydx_order_details)
            result["message"] = dydx_order_details["data"]["order"]
            order_manager.store_data(result["message"], "dydx_orders")
            return Response(result, status.HTTP_201_CREATED)
        except DydxApiError or ValueError as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    """
        method cancel  is used to cancel an given order on dydx .
        :param request will contain order Id to be cancelled.
        this method will call the dydx_client cancel_order function with given order id.
        :return cancel order details.
    """

    def cancel(self, request):
        self.serializer_class = CancelOrderRequestSerializer(data=request.data)
        self.serializer_class.is_valid(raise_exception=True)
        dydx_order = DydxOrder()
        order_manager = OrderManager()
        order_id = self.serializer_class.data["order_id"]
        result = {"message": None, "error": None}
        try:
            cancelled_order_details = dydx_order.cancel_order(order_id)
            cancelled_order_details = vars(cancelled_order_details)
            result["message"] = cancelled_order_details["data"]["cancelOrder"]
            order_manager.update_data(order_id, "dydx_orders", "CANCEL")
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            e = vars(e)
            print("this is error", e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    """ method dydx_order is responsible for getting all the openPositions on dydx .
        :return openPositions on dydx.
    """

    def dydx_order(self, request):
        result = {"message": None, "error": None}
        admin = DydxAdmin()

        try:
            orders = admin.get_account()
            orders = vars(orders)
            orders_data = orders["data"]["account"]["openPositions"]
            if not orders_data:
                raise Exception("No open position found on dydx")
            result["message"] = orders_data
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def orders(self, request):
        result = {"message": None, "error": None}
        request_data = request.query_params.dict()
        self.serializer_class = FirestoreOrdersRequestSerializer(data=request_data)
        self.serializer_class.is_valid(raise_exception=True)
        validated_data = self.serializer_class.data

        order_manager = OrderManager()

        try:
            orders = order_manager.fetch_orders(order_id=validated_data.get("order_id"))
            if orders is None:
                raise Exception("Order id not found")
            result["message"] = orders
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
