from decouple import config

from services import LoadContracts
from web3 import middleware, gas_strategies
from web3.gas_strategies import time_based

from utilities.constant import (
    SAMPLE_SIZE,
    MAX_WAIT_SECONDS,
    PROBABILITY,
    WALLET_ADDRESS,
    RINKEBY_CHAIN_ID,
)


class TransactionManager:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.w3 = self.load_contract.web3_provider()

    def sign_transactions(self, transaction):
        signed_transaction = self.w3.eth.account.sign_transaction(
            transaction, config("PRIVATE_KEY")
        )
        transaction_hash = self.w3.eth.send_raw_transaction(
            signed_transaction.rawTransaction
        )
        return str(self.w3.toHex(transaction_hash))

    def create_transaction(
        self, nonce, max_fee_per_gas, max_priority_fee_per_gas, from_account, chain_id
    ):
        transaction = {
            "type": "0x2",
            "nonce": nonce,
            "from": from_account,
            "maxFeePerGas": self.w3.toWei(max_fee_per_gas, "gwei"),
            "maxPriorityFeePerGas": self.w3.toWei(max_priority_fee_per_gas, "gwei"),
            "chainId": chain_id,
        }
        return transaction

    def transaction_gas_price(self, max_wait_seconds, sample_size, probability):
        price_strategy = self.get_gas_price_strategy(max_wait_seconds, sample_size, probability)
        self.w3.eth.set_gas_price_strategy(price_strategy)
        wei_price = self.w3.eth.generate_gas_price()
        price = self.w3.fromWei(wei_price, "gwei")
        return price

    @staticmethod
    def get_gas_price_strategy(max_wait_seconds, sample_size, probability, weighted=True):
        price_strategy = (
            gas_strategies.time_based.construct_time_based_gas_price_strategy(
                max_wait_seconds, sample_size, probability, weighted
            )
        )
        return price_strategy

    def build_transaction(self):
        gas_price = self.transaction_gas_price(MAX_WAIT_SECONDS, SAMPLE_SIZE, PROBABILITY)
        nonce = self.w3.eth.getTransactionCount(WALLET_ADDRESS)
        transaction = self.create_transaction(
            nonce, gas_price, gas_price, WALLET_ADDRESS, RINKEBY_CHAIN_ID
        )
        return transaction


if __name__ == "__main__":
    a = TransactionManager()
    print(a.transaction_gas_price(60, 2, 100))
