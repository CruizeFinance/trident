import ast
from decouple import config
from components import TransactionManager
from services import LoadContracts
from utilities.constant import WALLET_ADDRESS, LINK_ADDRESS, WALLET_ADDRESS_2
from utilities.enums.error_codes import ErrorCodes


class StarkExContract:
    def __init__(self):
        self.load_contract = LoadContracts()
        self.transaction_manager = TransactionManager()

        contract_abi = open("../contract_abis/dydx_starkware_perpetuals.json")
        self.contract = self.load_contract.load_contracts(
            config("STARK_EX_CONTRACT"), contract_abi
        )
        self.w3 = self.load_contract.web3_provider()

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
        signed_tx = self.transaction_manager.sign_transactions(transaction)
        return signed_tx

    def send(self, amount, max_fee_per_gas, max_priority_fee_per_gas, chain_id):
        result = {"transaction": None, "error": None}
        try:
            nonce = self.w3.eth.getTransactionCount(WALLET_ADDRESS)
            print("nonce", nonce)
            # will change for mainnet
            contract_abi = open("../contract_abis/Link.json")
            load = LoadContracts()
            sc = load.load_contracts(LINK_ADDRESS, contract_abi)
            transaction = self.transaction_manager.create_transaction(
                nonce,
                max_fee_per_gas,
                max_priority_fee_per_gas,
                WALLET_ADDRESS,
                chain_id,
            )
            contract_transaction = sc.functions.transfer(
                WALLET_ADDRESS_2,  # will change for mainnet
                self.w3.toWei(amount, "ether"),
            ).buildTransaction(transaction)
            tnx = self.transaction_manager.sign_transactions(contract_transaction)
            result["transaction"] = tnx
            return result
        except ValueError as e:
            e = str(e)
            e = ast.literal_eval(e)
            print(e)
            error = e["message"]
            if error == ErrorCodes.nonce_to_low.value["error_code"]:
                result["error"] = ErrorCodes.nonce_to_low.value["message"]
                return result
            elif error == ErrorCodes.already_known.value["error_code"]:
                result["error"] = ErrorCodes.already_known.value["message"]
                return result
            elif error == ErrorCodes.invalid_opcode.value["error_code"]:
                result["error"] = ErrorCodes.invalid_opcode.value["message"]
                return result
            else:
                result["error"] = error
                return result
        except Exception as e:
            result["error"] = e
            return result


if __name__ == "__main__":
    a = StarkExContract()
    print(
        a.send(
            amount=1,
            max_fee_per_gas=1.544000081,
            max_priority_fee_per_gas=1.544000081,
            chain_id=4,
        )
    )
# 1770000009
