from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from cruize_operations import AmountSerializers
from services.contracts.cruize.cruize_contract import Cruize


class CruizeOperations(GenericViewSet):
    def repay_to_aave(self, request):
        self.serializer_class = AmountSerializers
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data
        cruize_ref = Cruize()
        try:
            result = "passs"
            # result = cruize_ref.repay_to_aave(amount)
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def deposit_to_cruize(self, request):
        self.serializer_class = AmountSerializers
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data
        cruize_ref = Cruize()
        try:
            result = "passs"
            # result = cruize_ref.deposit_to_cruize(amount)
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status.HTTP_500_INTERNAL_SERVER_ERROR)
