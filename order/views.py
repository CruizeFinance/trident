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
        try:
            response = DYDX_ORDER.create_order(order_data)
            response = vars(response)
            response = response["data"]["order"]
            return Response(response, status.HTTP_201_CREATED)
        except DydxApiError or ValueError as e:
            e = vars(e)
            error = e["msg"]["errors"][0]["msg"]
            error_codes = ErrorCodes
            if error_codes.signature_error.value == error:
                return Response(str("Invalid position id"), status.HTTP_400_BAD_REQUEST)
            return Response(str(error), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

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
        try:
            response = DYDX_ORDER.cancel_order(order_id)
            response = vars(response)
            response = response["data"]["cancelOrder"]
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            e = vars(e)
            error = e["msg"]["errors"][0]["msg"]
            return Response(str(error), status.HTTP_400_BAD_REQUEST)

    def get_position_id(self, requset):
        try:
            position_id = ADMIN.get_position_id()
            return Response("position_id:" + str(position_id), status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
