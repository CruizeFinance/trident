import json

from web3 import Web3
from decouple import config

from services import LoadContracts

class StarkExContract:
    def __init__(self):
        self.load_contract = LoadContracts()
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
        signed_tx = self.w3.eth.account.sign_transaction(
            transaction, config("PRIVATE_KEY")
        )
        txn_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("Waiting for transaction to be confirmed...")
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        print(txn_receipt)
    def tn1x(self):

        from_account = '0xE0E24a32A7e50Ea1c7881c54bfC1934e9b50B520'
        to_account =  Web3.toChecksumAddress("0x6617bd03132bc4212c0d719734cb56ca44b54d61")
        nonce = self.w3.eth.getTransactionCount(from_account)
        print(nonce)
        tx = {
            'type': '0x2',
            'nonce': nonce,
            'from': from_account,
            'maxFeePerGas': self.w3.toWei('2', 'gwei'),
            'maxPriorityFeePerGas': self.w3.toWei('1', 'gwei'),
            'chainId': 4,
            # "gasPrice":self.w3.toWei('1', 'gwei')
        }
        gas = self.w3.eth.estimateGas(tx)
        print(gas)

        # tx['gas'] = gas*2
        contract_abi = open("../contract_abis/Link.json")
        link_address = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
        load = LoadContracts()
        sc = load.load_contracts(link_address, contract_abi)
        print("tx gas",sc.functions.transfer(
            "0xBD43b05ac20F96B808d3c644c3CF7add86ad5F58",
            self.w3.toWei(10, 'ether'),
        ).estimate_gas({ "from": from_account }))
        tnx = sc.functions.transfer(
            "0xBD43b05ac20F96B808d3c644c3CF7add86ad5F58",
            self.w3.toWei(10, 'ether'),

        ).buildTransaction(
            tx
        )

        hash = "0x8fddae49f5601a0bfd6933f02c70119b1a75e3e6fd2397f7dd277e2a999b564d"
        # transaction = self.w3.eth.modify_transaction(hash).buildTransaction()
        # transaction.update(
        #     tx
        # )
        signed_tx = self.w3.eth.account.sign_transaction(tnx, config("PRIVATE_KEY"))
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("Transaction hash: " + str(self.w3.toHex(tx_hash)))

if __name__ == '__main__':
    a =  StarkExContract()
    a.tn1x()