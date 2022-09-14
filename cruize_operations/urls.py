from django.urls import path

from cruize_operations.views import CruizeOperations

urlpatterns = [
    path("deposit", CruizeOperations.as_view({"post": "deposit_to_cruize"})),
    path("repay", CruizeOperations.as_view({"post": "repay_to_aave"})),
]
