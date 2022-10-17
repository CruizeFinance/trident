from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from components import PriceFloorManager, FirebaseDataManager
from cruize_operations import (
    RepayToAaveRequestSerializer,
    CruizeDepositRequestSerializer,
    FirebaseRequestSerializer,
    FirebaseFecthRequestSerializer,
    SetPriceFloorSerializer,
)
from services.avve_asset_apy import AaveApy
from services.contracts.cruize.cruize_contract import Cruize
from utilities import cruize_constants
price_floor_manager = PriceFloorManager()



class CruizeOperations(GenericViewSet):
    def repay_to_aave(self, request):
        result = {"message": None, "error": None}
        self.cruize_contract_ref = Cruize()
        self.serializer_class = RepayToAaveRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data
        try:
            result["message"] = self.cruize_contract_ref.repay_to_aave(amount)

            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit(self, request):
        self.cruize_contract_ref = Cruize()
        result = {"message": None, "error": None}
        self.serializer_class = CruizeDepositRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deposit_data = serializer.data
        try:
            result["message"] = self.cruize_contract_ref.deposit_to_cruize(deposit_data)
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_transactions(self, request):
        result = {"message": None, "error": None}
        self.cruize_contract_ref = Cruize()
        self.serializer_class = FirebaseRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deposit_data = serializer.data
        firebase_db_obj = FirebaseDataManager()
        try:

            firebase_db_obj.store_sub_collections(
                deposit_data,
                cruize_constants.CRUIZE_USER,
                deposit_data["wallet_address"],
                "transactions",
                deposit_data["transaction_hash"],
            )
            result["message"] = "success"
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_user_transactions(self, request):
        result = {"message": None, "error": None}
        self.cruize_contract_ref = Cruize()
        request_body = request.query_params
        self.serializer_class = FirebaseFecthRequestSerializer

        serializer = self.serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            firebase_db_obj = FirebaseDataManager()
            result[
                "message"
            ] = firebase_db_obj.fetch_sub_collections(
                cruize_constants.CRUIZE_USER, data["wallet_address"], "transactions"
            )
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def price_floor(self, request):
        result = {"result": None, "error": None}
        try:

            result["result"] = price_floor_manager.assets_price_floor()
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_price_floor(self, request):
        self.serializer_class = SetPriceFloorSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset_data = serializer.data
        result = {"result": None, "error": None}
        try:

            result["result"] = price_floor_manager.set_price_floor(
                asset_data["asset_name"], asset_data["days"]
            )
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_asset_apy(self, request):
        result = {"result": None, "error": None}
        try:
            aave_apy_obj = AaveApy()
            result["result"] = aave_apy_obj.fetch_asset_apys()
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
