from django.urls import path

from cruize_operations.views import CruizeOperations

urlpatterns = [
    path("deposit", CruizeOperations.as_view({"post": "deposit"})),
    path("borrow", CruizeOperations.as_view({"post": "borrow"})),
    path("repay", CruizeOperations.as_view({"post": "repay"})),
    path("transaction/save", CruizeOperations.as_view({"post": "save_transactions"})),
    path(
        "transaction/fetch",
        CruizeOperations.as_view({"get": "fetch_user_transactions"}),
    ),
    path("price_floor", CruizeOperations.as_view({"get": "price_floor"})),
    path("price_floor/", CruizeOperations.as_view({"put": "set_price_floor"})),
    path("apy", CruizeOperations.as_view({"get": "fetch_asset_apy"})),
    path("asset_tvl", CruizeOperations.as_view({"post": "save_asset_tvl"})),
]
