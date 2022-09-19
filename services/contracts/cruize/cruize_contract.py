from decouple import config

from components import TransactionManager
from services import LoadContracts
from utilities import constants
from utilities.exception import ContractException


class Cruize:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.exception = ContractException()
        self.transaction_manager = TransactionManager()

        contract_abi = open("services/contracts/cruize/cruize_contract.json")
        self.contract = self.load_contract.load_contracts(
            constants.TEST_CRUIZE_CONTRACT_ADDRESS, contract_abi
        )
        self.w3 = self.load_contract.web3_provider()

    # this function will deposit to curize contract from our  curize wallet .
    def deposit_to_cruize(self, deposit_data):
        result = {"transaction_hash": None, "error": None}
        amount = deposit_data["amount"]
        asset_address = deposit_data["asset_address"]
        try:
            transaction = self.transaction_manager.build_transaction(
                constants.WALLET_ADDRESS, eth_value=amount
            )
            contract_transaction = self.contract.functions.deposit(
                self.w3.toWei(amount, "ether"), asset_address
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

    def withdraw_from_cruize(self, deposit_data):
        result = {"transaction_hash": None, "error": None}
        amount = deposit_data["amount"]
        asset_address = deposit_data["asset_address"]
        try:
            transaction = self.transaction_manager.build_transaction(
                constants.WALLET_ADDRESS
            )
            contract_transaction = self.contract.functions.withdraw(
                int(amount), asset_address
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

    def repay_to_aave(self, amount):
        amount = amount["amount"]
        result = {"transaction_hash": None, "error": None}
        try:
            transaction = self.transaction_manager.build_transaction(
                wallet_address=constants.TEST_OWNER_ADDRESS
            )
            contract_transaction = self.contract.functions.repay(
                int(amount)
            ).buildTransaction(transaction)
            tnx = self.transaction_manager.sign_transactions(
                contract_transaction, config("CONTRACT_OWNER_PRIVATE_KEY")
            )
            result["transaction_hash"] = tnx
            return result
        except ValueError as e:
            result["error"] = self.exception.validate_exceptions(e)
            return result
        except Exception as e:
            result["error"] = e
            return result
