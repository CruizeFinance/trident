from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from components.dydx_order_manager import DydxOrderManager
from order.serializers import (
    OrderRequestSerializer,
    CancelOrderRequestSerializer,
    FirestoreOrdersRequestSerializer,
    DydxAllOrdersRequestSerializer,
)
from services import DydxOrder, DydxAdmin
from settings_config import dydx_p_client_obj, asset_dydx_instance
from utilities.error_handler import ErrorHandler


class Order(GenericViewSet):
    """
     method create() is used to create order on dydx.
    :param - request will contain order details to place.
    this method will call the dydx_client method create_order with given params.
    :return order details that has been placed.
    """

    def initialize(self):
        self.dydx_order_obj = DydxOrder()
        self.error_handler = ErrorHandler()

    def create(self, request):
        self.initialize()
        self.serializer_class = OrderRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_data = serializer.data
        dydx_order_manager_obj = DydxOrderManager()
        result = {"message": None, "error": None}
        try:
            order_data = dydx_order_manager_obj.create_order_params(
                order_data["side"],
                order_data["market"],
                order_data["size"],
                order_data["price"],
                dydx_p_client_obj["side"],
            )

            dydx_order_details = self.dydx_order_obj.create_order(
                order_data, asset_dydx_instance["side"]
            )

            dydx_order_details = vars(dydx_order_details)
            result["message"] = dydx_order_details["data"]["order"]
            return Response(result, status.HTTP_201_CREATED)
        except DydxApiError or ValueError as e:
            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    """
        :method  - cancel  is used to cancel an given order on dydx .
        :param  -   request will contain order Id to be cancelled.this method will call the dydx_client cancel_order function with given order id.
        :return - cancel order details.
    """

    def cancel(self, request):
        self.initialize()
        self.serializer_class = CancelOrderRequestSerializer(data=request.data)
        self.serializer_class.is_valid(raise_exception=True)
        order_id = self.serializer_class.data["order_id"]
        result = {"message": None, "error": None}
        try:
            cancelled_order_details = self.dydx_order_obj.cancel_order(order_id)
            cancelled_order_details = vars(cancelled_order_details)
            result["message"] = cancelled_order_details["data"]["cancelOrder"]
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:

            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            e = vars(e)

            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    """ method dydx_order is responsible for getting all the openPositions on dydx .
        :return openPositions on dydx.
    """

    def dydx_order(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = DydxAllOrdersRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_data = serializer.data
        dydx_admin_obj = DydxAdmin()
        error_handler = ErrorHandler()
        try:
            orders = dydx_admin_obj.get_account(validate_data["type"])
            orders = vars(orders)
            orders_data = orders["data"]["account"]["openPositions"]
            if not orders_data:
                raise Exception("No open position found on dydx")
            result["message"] = orders_data
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            result["error"] = error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            e = vars(e)
            if e["msg"]:
                result["error"] = e["msg"]["errors"][0]["msg"]
            else:
                result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def orders(self, request):
        result = {"message": None, "error": None}
        request_data = request.query_params.dict()
        self.serializer_class = FirestoreOrdersRequestSerializer(data=request_data)
        self.serializer_class.is_valid(raise_exception=True)
        validated_data = self.serializer_class.data
        dydx_order_manager_obj = DydxOrderManager()
        try:
            orders = dydx_order_manager_obj.price_floor_manager_obj.firebase_data_manager_obj.fetch_orders(
                order_id=validated_data.get("order_id")
            )
            if orders is None:
                raise Exception("Order id not found")
            result["message"] = "order"
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
