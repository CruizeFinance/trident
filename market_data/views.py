from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from market_data.serializers import (
    MarketDataDayRequestSerializer,
    MarketDataTimestampRequestSerializer,
)
from services.market_data import coingecko


class MarketData(GenericViewSet):
    def market_chart_day(self, request):
        result = {"prices": None, "error": None}
        self.serializer_class = MarketDataDayRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            market_chart_day_result = coingecko.market_chart_day(**data)
            result["prices"] = market_chart_day_result["prices"]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def market_chart_timestamp(self, request):
        result = {"prices": None, "error": None}
        print(request)
        self.serializer_class = MarketDataTimestampRequestSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            market_chart_day_result = coingecko.market_chart_timestamp(**data)
            result["prices"] = market_chart_day_result["prices"]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)