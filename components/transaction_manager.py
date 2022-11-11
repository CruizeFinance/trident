from web3 import gas_strategies
from web3.gas_strategies import time_based

from services.contracts import LoadContracts
from utilities import cruize_constants

"""class :: TransactionManager -  is used to manage the on chain transactions for our dydx wallets."""


class TransactionManager:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.w3 = self.load_contract.web3_provider()

    """
       method :: sign_transactions - is used to sing transactions for wallets.
       params :: transaction -  is the transaction details.
       params :: private_key - private key of cruize wallet.
       returns :: sing transaction.
    """

    def sign_transactions(self, transaction, private_key):
        signed_transaction = self.w3.eth.account.sign_transaction(
            transaction, private_key
        )
        transaction_hash = self.w3.eth.send_raw_transaction(
            signed_transaction.rawTransaction
        )
        return str(self.w3.toHex(transaction_hash))

    """
          method :: create_transaction - is used to create transactions for wallets.
          params :: nonce -  nonce of cruize wallets.
          params :: private_key - private key of cruize wallet.
          params ::  max_fee_per_gas - max fee per gas for transactions.
          params :: from_account - wallet address.
          params :: chain_id - id for chain.
          params ::  eth_value - value of eth in the transactions.
          return :: transaction.
          
       """

    def create_transaction(
        self,
        nonce,
        max_fee_per_gas,
        max_priority_fee_per_gas,
        from_account,
        chain_id,
        eth_value,
    ):
        transaction = {
            "type": "0x2",
            "nonce": nonce,
            "from": from_account,
            "maxFeePerGas": self.w3.toWei(max_fee_per_gas, "gwei"),
            "maxPriorityFeePerGas": self.w3.toWei(max_priority_fee_per_gas, "gwei"),
            "chainId": chain_id,
        }
        if eth_value is not None:
            transaction["value"] = self.w3.toWei(eth_value, "ether")
        return transaction

    """
        method :: transaction_gas_price - is used to predict the transactions  gas fee.
        returns ::transaction gas price.
     """

    def transaction_gas_price(self, max_wait_seconds, sample_size, probability):
        price_strategy = self.get_gas_price_strategy(
            max_wait_seconds, sample_size, probability
        )
        self.w3.eth.set_gas_price_strategy(price_strategy)
        wei_price = self.w3.eth.generate_gas_price()
        price = self.w3.fromWei(wei_price, "gwei")
        return price

    @staticmethod
    def get_gas_price_strategy(
        max_wait_seconds, sample_size, probability, weighted=True
    ):
        price_strategy = (
            gas_strategies.time_based.construct_time_based_gas_price_strategy(
                max_wait_seconds, sample_size, probability, weighted
            )
        )
        return price_strategy

    """
        method :: build_transaction  - is used to build the transactions .
        params :: wallet_address - wallet address of cruize wallet.
        returns :: build transaction 
     """

    def build_transaction(self, wallet_address, eth_value=None):
        gas_price = self.transaction_gas_price(
            cruize_constants.MAX_WAIT_SECONDS,
            cruize_constants.BLOCK_SAMPLE_SIZE,
            cruize_constants.PROBABILITY,
        )
        nonce = self.w3.eth.getTransactionCount(wallet_address)
        transaction = self.create_transaction(
            nonce,
            gas_price,
            gas_price,
            wallet_address,
            cruize_constants.MAINNET_CHAIN_ID,
            eth_value,
        )
        return transaction


if __name__ == "__main__":
    a = TransactionManager()
    print(a.transaction_gas_price(60, 2, 100))
