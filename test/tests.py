import time

from django.test import TestCase

from services.celery.celery import open_order_on_dydx, close_order_on_dydx
from services.contracts.cruize.cruize_contract import Cruize


class TestCruizeWorkflow(TestCase):
    def test_deposit_cruize(self):
        self.cruize = Cruize()
        data = self.cruize.deposit_to_cruize(
            {
                "amount": "0.01",
                "asset_address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            }
        )
        time.sleep(30)
        print("deposit to cruize", data)

    def test_deposit_dydx(self):
        data = self.client.post("/dydx_operations/deposit/test")
        print("deposit to dydx", data)

    def test_open_and_close_position(self):
        open_order_on_dydx("1500")
        time.sleep(30)
        close_order_on_dydx("1500")

    def test_repay_cruize(self):
        self.cruize = Cruize()
        data = self.cruize.repay_to_aave({"amount": "5000000"})
        time.sleep(30)
        print("repay to aave", data)

    def test_withdrawal_from_cruize(self):
        self.cruize = Cruize()
        data = self.cruize.withdraw_from_cruize(
            {
                "amount": "10000000000000000",
                "asset_address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            }
        )
        print("withdraw from cruzie", data)
