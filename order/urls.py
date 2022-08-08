from django.urls import path

from order.views import Order

urlpatterns = [
    path("create", Order.as_view({"post": "create"})),
<<<<<<< HEAD
<<<<<<< HEAD
    path("cancel", Order.as_view({"post": "cancel"})),
    path("", Order.as_view({"get": "dydx_order"})),
    path("firestore", Order.as_view({"get": "orders"})),
=======
    path("cancel", Order.as_view({"post": "cancel"}))
>>>>>>> 68fe6e3 (write methods for storing and updating data on db)
=======
    path("cancel", Order.as_view({"post": "cancel"})),
    path("", Order.as_view({"get": "dydx_order"})),
>>>>>>> 0a98c22 (create api for getting user's order information minor change in order_serializer)
]
