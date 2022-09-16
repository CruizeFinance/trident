from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from components import OrderManager
from dydx_operations import (
    SlowWithdrawalSerializer,
    FastWithdrawalSerializer,
    TransferSerializer,
    DepositSerializer,
)

from services import DydxWithdrawal, DydxAdmin
from services.contracts.dydx_starkex.dydx_starkex_contract import DydxStarkExContract


class DydxOprations(GenericViewSet):
    """function slow withdrawal is responsible for withdrawing user's asset's.
    :returns DydxOprations information.
    """

    def slow_withdrawal(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = SlowWithdrawalSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            order_manager_obj = OrderManager()
            dydx_withdrawal_obj = DydxWithdrawal()
            withdrawal_data = dydx_withdrawal_obj.slow_withdrawal(data)
            result["message"] = withdrawal_data["data"]["withdrawal"]
            result["message"]["address"] = data["user_address"]
            order_manager_obj.store_data(result["message"], "withdrawal")
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fast_withdrawal(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = FastWithdrawalSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        withdrawal_data = serializer.data
        try:
            dydx_withdrawal_obj = DydxWithdrawal()
            withdrawal_data = dydx_withdrawal_obj.fast_withdrawal(withdrawal_data)

            result["message"] = withdrawal_data.get("withdrawal")
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit(self, request):
        self.serializer_class = DepositSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            stark_ex_contract_ref = DydxStarkExContract()
            deposit_data = stark_ex_contract_ref.deposit(data)
            return Response(deposit_data, status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)

    """ :return user transfer history."""

    def transfer_information(self, request):
        result = {"message": None, "error": None}
        self.serializer_class = TransferSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            dydx_withdrawal_obj = DydxWithdrawal()
            transfer_data = dydx_withdrawal_obj.all_transfer_details(data)
            result["message"] = transfer_data["data"]["transfers"]
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit_test_fund(self, request):
        result = {"message": None, "error": None}
        dydx_admin_obj = DydxAdmin()
        try:
            fund_details = dydx_admin_obj.deposit_fund()
            result["message"] = fund_details["data"]["transfer"]
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
