from django.urls import path

from market_data.views import MarketData

urlpatterns = [
    path("asset_price", MarketData.as_view({"get": "asset_price"})),
]
