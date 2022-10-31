from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from components import PriceFloorManager, FirebaseDataManager, CruizeDataManager
from cruize_operations import (
    RepayToAaveRequestSerializer,
    CruizeDepositRequestSerializer,
    FirebaseRequestSerializer,
    FirebaseFecthRequestSerializer,
    SetPriceFloorSerializer,
)
from cruize_operations.serilaizer import Tvl_Serializer
from services.avve_asset_apy import AaveApy
from services.contracts.cruize.cruize_contract import Cruize
from utilities import cruize_constants

price_floor_manager = PriceFloorManager()


class CruizeOperations(GenericViewSet):
    def repay_to_aave(self, request):
        result = {"message": None, "error": None}
        cruize_contract_ref = Cruize()
        serializer_class = RepayToAaveRequestSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data
        try:
            result["message"] = cruize_contract_ref.repay_to_aave(amount)

            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit(self, request):
        cruize_contract_ref = Cruize()
        result = {"message": None, "error": None}
        serializer_class = CruizeDepositRequestSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deposit_data = serializer.data
        try:
            result["message"] = cruize_contract_ref.deposit_to_cruize(deposit_data)
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_transactions(self, request):
        result = {"message": None, "error": None}
        serializer_class = FirebaseRequestSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deposit_data = serializer.data
        firebase_db_obj = FirebaseDataManager()

        try:
            firebase_db_obj.store_sub_collections(
                data=deposit_data,
                collection="cruize_users",
                document_name=deposit_data["wallet_address"],
                sub_collection="transactions",
                sub_document=deposit_data["transaction_hash"],
            )
            result["message"] = "success"
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_user_transactions(self, request):
        result = {"message": None, "error": None}
        request_body = request.query_params
        serializer_class = FirebaseFecthRequestSerializer

        serializer = serializer_class(data=request_body)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        try:
            firebase_db_obj = FirebaseDataManager()
            firebase_data = firebase_db_obj.fetch_sub_collections(
                cruize_constants.CRUIZE_USER, data["wallet_address"], "transactions"
            )
            if not firebase_data:
                raise ValidationError(
                    f"No data found for wallet address: {data['wallet_address']}"
                )

            data = []
            if data is not None:
                for tnx_data in firebase_data:
                    data.append(tnx_data.to_dict())
            result["message"] = data

            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def price_floor(self, request):
        result = {"result": None, "error": None}
        try:

            result["result"] = price_floor_manager.get_assets_price_floors()
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_price_floor(self, request):
        serializer_class = SetPriceFloorSerializer
        serializer = serializer_class(data=request.data)
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
    def save_stacked_asset_amount(self,request):
        serializer_class = Tvl_Serializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset_data = serializer.data
        result = {"result": None, "error": None}
        try:
         cruize_data_manager_obj  =    CruizeDataManager()
         cruize_data_manager_obj.save_TVL(asset_data)
         result['result'] = 'success'
         return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

