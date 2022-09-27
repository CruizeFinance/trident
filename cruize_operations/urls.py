from django.urls import path

from cruize_operations.views import CruizeOperations

urlpatterns = [
    path("deposit", CruizeOperations.as_view({"post": "deposit"})),
    path("borrow", CruizeOperations.as_view({"post": "borrow"})),
    path("repay", CruizeOperations.as_view({"post": "repay"})),
    path("transaction/store", CruizeOperations.as_view({"post": "save_transactions"})),
    path("transaction/fetch", CruizeOperations.as_view({"post": "fetch_user_transactions"})),
]
