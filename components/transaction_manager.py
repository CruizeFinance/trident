from decouple import config

from services import LoadContracts


class TransationManager:
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
