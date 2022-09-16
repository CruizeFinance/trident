import ast

from utilities.enums import ErrorCodes


class ContractException:
    def validate_exceptions(self, e):

        e = str(e)
        e = ast.literal_eval(e)
        print(e)
        error = e["message"]
        if error == ErrorCodes.nonce_to_low.value["error_code"]:
            return ErrorCodes.nonce_to_low.value["message"]
        elif error == ErrorCodes.already_known.value["error_code"]:
            return ErrorCodes.already_known.value["message"]
        elif error == ErrorCodes.invalid_opcode.value["error_code"]:
            return ErrorCodes.invalid_opcode.value["message"]
        else:
            return e
