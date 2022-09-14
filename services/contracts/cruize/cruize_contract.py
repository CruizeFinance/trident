import ast

from decouple import config
from components import TransactionManager
from services import LoadContracts, DydxAdmin
from settings_config import contract_exceptions
from utilities.constant import (
    WALLET_ADDRESS,
    RINKEBY_CHAIN_ID,
    PROBABILITY,
    SAMPLE_SIZE,
    MAX_WAIT_SECONDS,
)
from utilities.enums import ErrorCodes


class Cruize:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.transaction_manager = TransactionManager()
        # will change once our contract is deployed .
        contract_abi = open("services/contracts/contract_abis/Starkware.json")
        self.contract = self.load_contract.load_contracts(
            config("STARK_EX_CONTRACT"), contract_abi
        )
        self.w3 = self.load_contract.web3_provider()

    # this function will deposit to cruzie contract from our  curize wallet .
    def deposit_to_cruize(self, amount=None):
        result = {"transaction_hash": None, "error": None}
        amount = amount["amount"]

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
            return contract_exceptions.contract_exceptions(e)
        except Exception as e:
            result["error"] = e
            return result

    def repay_to_aave(self, amount):
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
            return contract_exceptions.contract_exceptions(e)
        except Exception as e:
            result["error"] = e
            return result
