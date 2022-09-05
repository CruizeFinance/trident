from django.urls import path
from dydx_operations.views import DydxOprations

urlpatterns = [
    path("slow", DydxOprations.as_view({"post": "slow_withdrawal"})),
    path("fast", DydxOprations.as_view({"post": "fast_withdrawal"})),
    path("transfer", DydxOprations.as_view({"get": "transfer_info"})),
    path("deposit", DydxOprations.as_view({"post": "deposit"})),
    path("deposit/test", DydxOprations.as_view({"post": "deposit_test_fund"})),
]
