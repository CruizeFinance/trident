from decouple import config
from components import TransactionManager
from services import LoadContracts, DydxAdmin
from utilities.exception import ContractException


class DydxStarkExContract:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.exception = ContractException()
        self.transaction_manager = TransactionManager()
        contract_abi = open(
            "services/contracts/dydx_starkex/dydx_starkware_contract.json"
        )
        self.contract = self.load_contract.load_contracts(
            config("STARK_EX_CONTRACT"), contract_abi
        )
        self.w3 = self.load_contract.web3_provider()

    """function withdraw will withdraw funds form dydx contract"""

    def withdraw(self):
        result = {"transaction_hash": None, "error": None}
        try:
            transaction = self.transaction_manager.build_transaction()
            transaction = self.contract.functions.withdraw(
                starkKey=int(config("STARK_PUBLIC_KEY"), 16),
                assetType=config("ASSET_TYPE"),
            ).buildTransaction(transaction)
            signed_tx = self.transaction_manager.sign_transactions(transaction)
            return signed_tx

        except ValueError as e:
            result["error"] = self.exception.validate_exceptions(e)
            return result

        except Exception as e:
            result["error"] = e
            return result

    def deposit(self, amount_obj):
        result = {"transaction_hash": None, "error": None}
        amount = amount_obj["amount"]
        admin = DydxAdmin()
        position_id = admin.get_position_id()
        try:
            transaction = self.transaction_manager.build_transaction()
            contract_transaction = self.contract.functions.deposit(
                self.w3.toWei(amount, "ether")
            ).buildTransaction(transaction)
            tnx = self.transaction_manager.sign_transactions(contract_transaction)
            result["transaction_hash"] = tnx
            return result
        except ValueError as e:
            result["error"] = self.exception.validate_exceptions(e)
            return result
        except Exception as e:
            result["error"] = e
            return result


if __name__ == "__main__":
    a = DydxStarkExContract()
    print(a.deposit({"amount": 1}))
