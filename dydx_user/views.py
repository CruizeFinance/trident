from dydx3 import DydxApiError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from services import DydxAdmin
from utilities.error_handler import ErrorHandler


class User(GenericViewSet):
    def initialize(self):
        self.dydx_admin_obj = DydxAdmin()
        self.error_handler = ErrorHandler()

    def position_id(self, request):
        self.initialize()
        result = {"message": None, "error": None}
        try:
            position_id = self.dydx_admin_obj.get_position_id()
            result["message"] = {"position_id": position_id}
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def register_user(self, request):
        self.initialize()
        result = {"message": None, "error": None}
        try:
            user = self.dydx_admin_obj.register_user()
            if user is None:
                raise Exception("Fail to register")
            result["message"] = user["data"]["signature"]
            return Response(result, status.HTTP_200_OK)
        except DydxApiError or ValueError as e:
            result["error"] = self.error_handler.dydx_error_decoder(e)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
