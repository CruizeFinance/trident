from decouple import config
from components import TransactionManager
from services import LoadContracts
from utilities.exception import ContractException


class Cruize:
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

    # this function will deposit to curize contract from our  curize wallet .
    def deposit_to_cruize(self, amount=None):
        result = {"transaction_hash": None, "error": None}
        amount = amount["amount"]

        # need to pre-calculate the  gas price
        try:

            transaction = self.transaction_manager.build_transaction()
            contract_transaction = ""
            # self.contract.functions.deposit(
            #     self.w3.toWei(amount, "ether"),
            #     int(config("STARK_PUBLIC_KEY"), 16),
            #     position_id,
            #     SIGNATURE,
            # ).buildTransaction(transaction)
            tnx = self.transaction_manager.sign_transactions(contract_transaction)
            result["transaction_hash"] = tnx
            return result
        except ValueError as e:
            result["error"] = self.exception.validate_exceptions(e)
            return result
        except Exception as e:
            result["error"] = e
            return result

    def borrow_from_aave(self, amount):
        amount = amount["amount"]
        result = {"transaction_hash": None, "error": None}
        # need to pre calculate the price
        # average apis call time 20s
        try:
            transaction = self.transaction_manager.build_transaction()

            contract_transaction = ""
            # self.contract.functions.deposit(
            #     self.w3.toWei(amount, "ether"),
            #     int(config("STARK_PUBLIC_KEY"), 16),
            #     position_id,
            #     SIGNATURE,
            # ).buildTransaction(transaction)
            tnx = self.transaction_manager.sign_transactions(contract_transaction)
            result["transaction_hash"] = tnx
            return result
        except ValueError as e:
            result["error"] = self.exception.validate_exceptions(e)
            return result
        except Exception as e:
            result["error"] = e
            return result

    def repay_to_aave(self, amount):
        amount = amount["amount"]
        result = {"transaction_hash": None, "error": None}
        # need to pre-calculate the  gas price

        try:
            transaction = self.transaction_manager.build_transaction()

            contract_transaction = ""
            # self.contract.functions.deposit(
            #     self.w3.toWei(amount, "ether"),
            #     int(config("STARK_PUBLIC_KEY"), 16),
            #     position_id,
            #     SIGNATURE,
            # ).buildTransaction(transaction)
            tnx = self.transaction_manager.sign_transactions(contract_transaction)
            result["transaction_hash"] = tnx
            return result
        except ValueError as e:
            result["error"] = self.exception.validate_exceptions(e)
            return result
        except Exception as e:
            result["error"] = e
            return result
