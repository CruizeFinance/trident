import pytz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from components import FirebaseDataManager, PriceFloorManager
from cruize_operations import (
    RepayToAaveRequestSerializer,
    CruizeDepositRequestSerializer,
    FirebaeRequestSerializer,
    FirebaseFecthRequestSerializer, PriceFloorSerializer,
)
from datetime import  datetime
from services.contracts.cruize.cruize_contract import Cruize
from utilities import cruize_constants

class CruizeOperations(GenericViewSet):
    def initialize(self):
        self.cruize_contract_ref = Cruize()

    def repay_to_aave(self, request):
        result = {"message": None, "error": None}
        self.initialize()
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
        self.initialize()
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
        self.initialize()
        self.serializer_class = FirebaeRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        deposit_data = serializer.data
        try:
            self.firebase_data_manager_obj = FirebaseDataManager()
            self.firebase_data_manager_obj.store_data(
                deposit_data, cruize_constants.CRUIZE_USER
            )
            result["message"] = "success"
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_user_transactions(self, request):
        result = {"message": None, "error": None}
        self.initialize()
        self.serializer_class = FirebaseFecthRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            self.firebase_data_manager_obj = FirebaseDataManager()
            result["message"] = self.firebase_data_manager_obj.fetch_transaction_data(
                cruize_constants.CRUIZE_USER, data
            )
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = e
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def price_floor(self, request):
        self.serializer_class = PriceFloorSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset_data = serializer.data
        result = {'result': None, 'error': None}
        current_time = datetime.today()
        utc = pytz.UTC
        current_time = current_time.replace(tzinfo=utc)
        firebase_data_manager_obj = FirebaseDataManager()
        data = firebase_data_manager_obj.get_positions_status(asset_data['asset_name'], 'Position_data')
        if data is not None:
            data = data.to_dict()
        price_floor_manager_obj = PriceFloorManager()
        # try:
        if data is None:
            result['result'] = price_floor_manager_obj.calculate_price_floor(asset_data['asset_name'], asset_data['days'])
            return Response(result, status.HTTP_200_OK)
        price_floor_date = data["price_floor_time"]
        price_floor_date = price_floor_date.replace(tzinfo=utc)
        # price_floor_date = datetime.strptime(str(price_floor_date), '%Y-%m-%d')
        if  current_time > price_floor_date :
            result['result'] =  price_floor_manager_obj.calculate_price_floor(asset_data['asset_name'], asset_data['days'])
            return Response(result, status.HTTP_200_OK)
        result['result'] = data["price_floor"]
        return Response(result, status.HTTP_200_OK)
        # except Exception as e:
        #     result["error"] = e
        #     return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


