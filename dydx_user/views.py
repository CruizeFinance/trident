from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from services import DydxAdmin


class User(GenericViewSet):
    def position_id(self, request):
        result = {"message": None, "error": None}
        admin = DydxAdmin()
        try:
            position_id = admin.get_position_id()
            result["message"] = {"position_id": position_id}
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            e = vars(e)

            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def register_user(self, request):
        result = {"message": None, "error": None}
        admin = DydxAdmin()
        try:
            user = admin.register_user()
            if user is None:
                raise Exception("Fail to register")
            result["message"] = user["data"]["signature"]
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit_test_fund(self, request):
        result = {"message": None, "error": None}
        admin = DydxAdmin()
        try:
            fund_detiels = admin.deposit_fund()
            result["message"] = fund_detiels["data"]["transfer"]
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            e = vars(e)
            result["error"] = e["msg"]["errors"][0]["msg"]
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
