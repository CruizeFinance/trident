from django.urls import path

from market_data.views import MarketData

urlpatterns = [
    path("day/", MarketData.as_view({"post": "market_chart_day"})),
    path("timestamp/", MarketData.as_view({"post": "market_chart_timestamp"})),
]
