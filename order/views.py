from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from order.serializers import OrderRequestSerializer, CancelOrderRequestSerializer
from services import DydxAdmin, DydxOrder
from utilities.enums import ErrorCodes

ADMIN = DydxAdmin()
DYDX_ORDER = DydxOrder()


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

        result = {"message": None, "error": None}
        try:
            dydx_order_details = DYDX_ORDER.create_order(order_data)
            dydx_order_details = vars(dydx_order_details)
            result["message"] = dydx_order_details["data"]["order"]
            return Response(result, status.HTTP_201_CREATED)
        except DydxApiError or ValueError as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            error_codes = ErrorCodes
            if error_codes.signature_error.value == result["error"]:
                return Response(result, status.HTTP_400_BAD_REQUEST)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)

    """
        method cancel  is used to cancel an given order.
        :param request will contain order Id to be deleted.
        this method will call the dydx_client cancel_order function with given order id.
        :return cancel order details.
    """

    def cancel(self, request):
        self.serializer_class = CancelOrderRequestSerializer(data=request.data)
        self.serializer_class.is_valid(raise_exception=True)
        order_id = self.serializer_class.data["order_id"]

        result = {"message": None, "error": None}
        try:
            cancelled_order_details = DYDX_ORDER.cancel_order(order_id)
            cancelled_order_details = vars(cancelled_order_details)
            result["message"] = cancelled_order_details["data"]["cancelOrder"]
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_position_id(self, request):
        result = {"message": None, "error": None}
        try:
            position_id = ADMIN.get_position_id()
            result["message"] = {"position_id": position_id}
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
