from django.urls import path

from dydx_user.views import User

urlpatterns = [
    path("position_id", User.as_view({"get": "position_id"})),
    path("register", User.as_view({"post": "register_user"})),
    path("deposit/test", User.as_view({"post": "deposit_test_fund"})),
]
