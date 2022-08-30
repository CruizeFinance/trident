from enum import Enum


class ErrorCodes(Enum):
    nonce_to_low = {
        "error_code": "nonce too low",
        "message": "Transaction already done",
    }
    already_known = {
        "error_code": "already known",
        "message": "Transaction is already in queue",
    }
    invalid_opcode = {
        "error_code": "invalid opcode: INVALID",
        "message": "wallet balance is insufficient",
    }
