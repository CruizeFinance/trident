from django.urls import path

from order.views import Order

urlpatterns = [
    path("create", Order.as_view({"post": "create"})),
    path("cancel", Order.as_view({"post": "cancel"})),
    path("position_id", Order.as_view({"get": "get_position_id"})),
]
