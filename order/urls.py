from django.urls import path

from order.views import Order

urlpatterns = [
    path("create", Order.as_view({"post": "create"})),
    path("cancel", Order.as_view({"post": "cancel"}))
]
