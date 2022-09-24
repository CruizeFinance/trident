from decouple import config
from components import TransactionManager
from services import LoadContracts, DydxAdmin
from utilities import cruize_constants
from utilities.error_handler import ErrorHandler

# class  - DydxStarkExContract: is responsible for interacting with Dydx StarkExContract
class DydxStarkExContract:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.exception = ErrorHandler()
        self.transaction_manager = TransactionManager()
        contract_abi = open(
            "services/contracts/dydx_starkex/dydx_starkware_contract.json"
        )
        self.contract = self.load_contract.load_contracts(
            config("STARK_EX_CONTRACT"), contract_abi
        )
        self.w3 = self.load_contract.web3_provider()

    """
      :method - withdraw:will withdraw fund from the stark Ex L2 contract.
      :return - transaction hash.
    """

    def withdraw(self):
        result = {"transaction_hash": None, "error": None}
        try:
            transaction = self.transaction_manager.build_transaction(
                wallet_address=cruize_constants.WALLET_ADDRESS
            )
            transaction = self.contract.functions.withdraw(
                starkKey=int(config("STARK_PUBLIC_KEY"), 16),
                assetType=config("ASSET_TYPE"),
            ).buildTransaction(transaction)
            signed_tx = self.transaction_manager.sign_transactions(
                transaction, config("PRIVATE_KEY")
            )
            return signed_tx

        except ValueError as e:
            result["error"] = self.exception.validate_exceptions(e)
            return result

        except Exception as e:
            result["error"] = e
            return result

    """
      :method - deposit:will withdraw fund from the stark Ex L2 contract.
      :parms  -  amount: amount in USDC to deposit.
      :return - transaction hash.
    """

    def deposit(self, amount_obj):
        result = {"transaction_hash": None, "error": None}
        amount = amount_obj["amount"]
        try:
            transaction = self.transaction_manager.build_transaction(
                wallet_address=cruize_constants.WALLET_ADDRESS
            )
            contract_transaction = self.contract.functions.deposit(
                self.w3.toWei(amount, "ether")
            ).buildTransaction(transaction)
            tnx = self.transaction_manager.sign_transactions(
                contract_transaction, config("PRIVATE_KEY")
            )
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
