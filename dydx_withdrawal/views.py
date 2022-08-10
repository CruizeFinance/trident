from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from components import OrderManager
from dydx_withdrawal import (
    SlowWithdrawalSerializer,
    FastWithdrawalSerializer,
    TransferSerializer,
)

from services import DydxWithdrawal
from utilities.enums import ErrorCodes


class Withdrawal(GenericViewSet):
    """function slow withdrawal is responsible for withdrawing user's asset's.
    :returns Withdrawal information.
    """

    def slow_withdrawal(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = SlowWithdrawalSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            db_ref = OrderManager()
            withdarwal_ref = DydxWithdrawal()
            withdrawal_data = withdarwal_ref.slow_withdrawal(data)
            result["message"] = withdrawal_data["data"]["withdrawal"]
            result["message"]["address"] = data["user_address"]
            db_ref.store_data_firebase(result["message"], "withdrawal")
            return Response(result, status.HTTP_200_OK)
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

    # NOTICE - NOT TESTED YET.
    def fast_withdrawal(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = FastWithdrawalSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        withdrawal_data = serializer.data
        try:
            withdrawal_ref = DydxWithdrawal()
            withdrawal_data = withdrawal_ref.fast_withdrawal(withdrawal_data)
            result["message"] = withdrawal_data["data"]["withdrawal"]
            return Response(result, status.HTTP_200_OK)
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

    """ :return user transfer history."""

    def transfer_info(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = TransferSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:

            transfer_ref = DydxWithdrawal()
            transfer_data = transfer_ref.transfer(data)
            result["message"] = transfer_data["data"]["transfers"]
            return Response(result, status.HTTP_200_OK)
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