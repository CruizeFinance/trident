from django.urls import path

from cruize_operations.views import CruizeOperations

urlpatterns = [
    path("deposit", CruizeOperations.as_view({"post": "deposit"})),
    path("borrow", CruizeOperations.as_view({"post": "borrow"})),
    path("repay", CruizeOperations.as_view({"post": "repay"})),
]
