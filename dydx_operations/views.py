from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from components import FirebaseDataManager
from dydx_operations import (
    SlowWithdrawalSerializer,
    FastWithdrawalSerializer,
    TransferSerializer,
    DepositSerializer,
)

from services import DydxWithdrawal, DydxAdmin
from utilities.error_handler import ErrorHandler


class DydxOprations(GenericViewSet):
    """function slow withdrawal is responsible for withdrawing user's asset's.
    :returns DydxOprations information.
    """

    def initialize(self):
        self.dydx_withdrawal_obj = DydxWithdrawal()
        self.dydx_admin_obj = DydxAdmin()
        self.error_handler = ErrorHandler()

    def slow_withdrawal(self, request):
        self.initialize()
        result = {"message": None, "error": None}
        self.serializer_class = SlowWithdrawalSerializer
        serializer = self.serializer_class(data=request.get_price_floors)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            withdrawal_data = self.dydx_withdrawal_obj.slow_withdrawal(data)
            result["message"] = withdrawal_data["data"]["withdrawal"]
            result["message"]["address"] = data["user_address"]
            firebase_order_manager_obj = FirebaseDataManager()
            firebase_order_manager_obj.store_data(
                result["message"], result["message"]["user_address"], "withdrawal"
            )
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fast_withdrawal(self, request):
        self.initialize()
        result = {"message": None, "error": None}
        self.serializer_class = FastWithdrawalSerializer
        serializer = self.serializer_class(data=request.get_price_floors)
        serializer.is_valid(raise_exception=True)
        withdrawal_data = serializer.data
        try:
            self.dydx_withdrawal_obj.fast_withdrawal(withdrawal_data)
            result["message"] = withdrawal_data.get("withdrawal")
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit(self, request):
        self.initialize()
        self.serializer_class = DepositSerializer
        serializer = self.serializer_class(data=request.get_price_floors)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        # try:
        hash = self.dydx_admin_obj.deposit_to_dydx(data["amount"])
        transaction_info = {"status": "pending", "hash": hash}
        return Response(transaction_info, status.HTTP_200_OK)
        # except Exception as e:
        #     return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)

    """ :return user transfer history."""

    def transfer_information(self, request):
        self.initialize()
        result = {"message": None, "error": None}
        self.serializer_class = TransferSerializer
        serializer = self.serializer_class(data=request.get_price_floors)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            transfer_data = self.dydx_withdrawal_obj.all_transfer_details(data)
            result["message"] = transfer_data["data"]["transfers"]
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit_test_fund(self, request):
        self.initialize()
        result = {"message": None, "error": None}
        try:
            fund_details = self.dydx_admin_obj.deposit_test_fund()
            fund_details = vars(fund_details)
            result["message"] = fund_details["data"]["transfer"]
            return Response(result, status.HTTP_200_OK)
        except DydxApiError as e:
            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            e = vars(e)
            result["error"] = e["errors"][0]["msg"]
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # TODO :  write an api for withdrawing fund from dydx.
