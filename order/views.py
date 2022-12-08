from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from components.dydx_order_manager import DydxOrderManager
from order.serializers import (
    OrderRequestSerializer,
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
                order_data["price"],dydx_p_client_obj["side"],
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

    """ method dydx_order is responsible for getting all the openPositions on dydx .
        :return openPositions on dydx.
    """

    def dydx_order(self, request):
        result = {"message": None, "error": None}
        dydx_admin_obj = DydxAdmin()
        error_handler = ErrorHandler()
        request_body = request.query_params
        serializer_class = DydxAllOrdersRequestSerializer
        serializer = serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            orders = dydx_admin_obj.get_account(asset_dydx_instance[data["type"]])
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
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

