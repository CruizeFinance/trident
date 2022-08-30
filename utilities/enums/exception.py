import ast

from utilities.enums import ErrorCodes


class ContractException:
    def contract_exceptions(self, e):
        result = {"transaction_hash": None, "error": None}
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
