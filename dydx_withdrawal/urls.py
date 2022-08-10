from django.urls import path

from dydx_withdrawal.views import Withdrawal

urlpatterns = [
    path("slow", Withdrawal.as_view({"post": "slow_withdrawal"})),
    path("fast", Withdrawal.as_view({"post": "fast_withdrawal"})),
    path("transfer", Withdrawal.as_view({"get": "transfer_info"})),
]