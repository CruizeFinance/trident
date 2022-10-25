from decouple import config

from components.transaction_manager import TransactionManager
from services.contracts import LoadContracts

from utilities import cruize_constants
from utilities.error_handler import ErrorHandler

# class - Cruize: is responsible for performing oprations on Cruize contract .
class Cruize:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.exception = ErrorHandler()
        self.transaction_manager = TransactionManager()
        contract_abi = open("services/contracts/cruize/cruize_contract.json")
        self.contract = self.load_contract.load_contracts(
            cruize_constants.TEST_CRUIZE_CONTRACT_ADDRESS, contract_abi
        )
        self.w3 = self.load_contract.web3_provider()

        """
          :method   - deposit_to_cruize: will  deposit fund to Cruize Contract from Cruize wallet.
          :params   - deposit_data:all necessary parameters to deposit fund .
          :return   - transactions hash. 
        """

    def deposit_to_cruize(self, deposit_data):
        result = {"transaction_hash": None, "error": None}
        amount = deposit_data["amount"]
        asset_address = deposit_data["asset_address"]
        try:
            transaction = self.transaction_manager.build_transaction(
                cruize_constants.WALLET_ADDRESS, eth_value=amount
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

    """
      :method   - withdraw_from_cruize: will  withdraw fund from Cruize Contract to Cruize wallet.
      :params   - withdraw_data:all necessary parameters to withdraw fund .
      :return   - transactions hash. 
    """

    def withdraw_from_cruize(self, withdraw_data):
        result = {"transaction_hash": None, "error": None}
        amount = withdraw_data["amount"]
        asset_address = withdraw_data["asset_address"]
        try:
            transaction = self.transaction_manager.build_transaction(
                cruize_constants.WALLET_ADDRESS
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

    """
      :method   - repay_to_aave: will  repay the lone to Aave. 
      :params   - amount:Usdc amount to repay.
      :return   - transactions hash. 
    """

    def repay_to_aave(self, amount):
        repay_amount = amount["amount"]
        result = {"transaction_hash": None, "error": None}
        try:
            transaction = self.transaction_manager.build_transaction(
                wallet_address=cruize_constants.TEST_OWNER_ADDRESS
            )
            contract_transaction = self.contract.functions.repay(
                int(repay_amount)
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
