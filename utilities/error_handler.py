import ast

from utilities.enums import ErrorCodes

# class - ErrorHandler :  Handles Errors
class ErrorHandler:
    """
    :method   -  validate_exceptions: validate the contract exceptions.
    :params   - error:error dict.
    """

    def validate_exceptions(self, error):
        error = str(error)
        error = ast.literal_eval(error)
        error = error["message"]
        if error == ErrorCodes.nonce_to_low.value["error_code"]:
            return ErrorCodes.nonce_to_low.value["message"]
        elif error == ErrorCodes.already_known.value["error_code"]:
            return ErrorCodes.already_known.value["message"]
        elif error == ErrorCodes.invalid_opcode.value["error_code"]:
            return ErrorCodes.invalid_opcode.value["message"]
        else:
            return error

    """
      :method - dydx_error_decoder: decodes dydx api errors.
    """

    def dydx_error_decoder(self, error):
        error = vars(error)
        return error["msg"]["errors"][0]["msg"]
