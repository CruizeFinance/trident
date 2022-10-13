
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from market_data.serializers import (
    MarketDataDayRequestSerializer,
    MarketDataTimestampRequestSerializer,
    AssetPriceRequestSerializer,
)
from services.market_data.coingecko import CoinGecko


class MarketData(GenericViewSet):

    def market_chart_day(self, request):
        result = {"prices": None, "error": None}
        coin_gecko = CoinGecko()
        self.serializer_class = MarketDataDayRequestSerializer
        serializer = self.serializer_class(data=request.get_price_floors)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            market_chart_day_result = coin_gecko.market_chart_day(**data)
            result["prices"] = market_chart_day_result["prices"]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def market_chart_timestamp(self, request):
        result = {"prices": None, "error": None}
        coin_gecko = CoinGecko()
        self.serializer_class = MarketDataTimestampRequestSerializer
        serializer = self.serializer_class(data=request.get_price_floors)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            market_chart_day_result = coin_gecko.market_chart_timestamp(**data)
            result["prices"] = market_chart_day_result["prices"]
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def asset_price(self, request):
        result = {"price": None, "error": None}
        self.serializer_class = AssetPriceRequestSerializer
        serializer = self.serializer_class(data=request.get_price_floors)
        serializer.is_valid(raise_exception=True)
        coin_gecko = CoinGecko()
        data = serializer.data
        try:
            asset_price = coin_gecko.asset_price(data)
            result["price"] = asset_price
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
