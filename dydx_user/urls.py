from django.urls import path

from dydx_user.views import User

urlpatterns = [
    path("position_id", User.as_view({"get": "position_id"})),
]
