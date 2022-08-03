import json

from django.test import TestCase


class OrderTests(TestCase):
    def test_get_position_id(self):
        response = self.client.get("/order/position_id")
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        response = self.client.post(
            "/order/create",
            {
                "position_id": "63981",
                "market": "ETH-USD",
                "side": "BUY",
                "order_type": "LIMIT",
                "post_only": "false",
                "size": "1",
                "price": "18",
                "limit_fee": "0.4",
                "expiration_epoch_seconds": "2013988637",
                "time_in_force": "GTT",
            },
        )
        orderdata = response._container[0].decode()
        orderdata = json.loads(orderdata)
        self.assertEqual(response.status_code, 201)

    def test_cancel_order(self):
        response = self.client.post(
            "/order/cancel",
            {
                "order_id": "0640d358920d7662f5f8082759f110b5a72b4c7a60920905b88318159d1cfd0"
            },
        )
        self.assertEqual(response.status_code, 200)
