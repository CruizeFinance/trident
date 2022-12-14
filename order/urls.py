from django.urls import path

from order.views import Order

urlpatterns = [
    path("create", Order.as_view({"post": "create"})),
    path("cancel", Order.as_view({"post": "cancel"})),
    path("", Order.as_view({"get": "dydx_order"})),
    path("firestore", Order.as_view({"get": "orders"})),
]
