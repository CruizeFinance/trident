import json

from web3 import Web3
from decouple import config


class StarkExContract:
    def __init__(self):
        dydxabi = open("dydx_starkware_perpetuals.json")
        dydxabi_data = json.load(dydxabi)

        self.w3 = Web3(Web3.HTTPProvider(config("WEB_PROVIDER")))
        self.contract = self.w3.eth.contract(
            address=config("STARK_EX_CONTRACT"), abi=dydxabi_data
        )

    """function withdraw will withdraw funds form dydx contract"""

    def withdraw(self):
        transaction = self.contract.functions.withdraw(
            starkKey=int(config("STRAK_PUBLIC_KEY"), 16), assetType=config("ASSET_TYPE")
        ).buildTransaction()
        transaction.update(
            {
                "from": config("ETH_ADDRESS"),
                "nonce": self.w3.eth.get_transaction_count(config("ETH_ADDRESS")),
            }
        )
        signed_tx = self.w3.eth.account.sign_transaction(
            transaction, config("PRIVATE_KEY")
        )
        txn_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("Waiting for transaction to be confirmed...")
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        print(txn_receipt)
