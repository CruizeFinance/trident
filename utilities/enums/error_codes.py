import enum


class ErrorCodes(enum.Enum):
    signature_error = "Invalid signature for order"
    time_expiration_error = (
        "Order expiration cannot be less than 1 minute(s) in the future"
    )
    timeInForce_error = (
        "Invalid timeInForce is either not a string or not a valid time in force"
    )
    order_size_error = (
        "size must be a positive numeric string that is not greater than 1000000000"
    )
    price_size_error = (
        "price must be a positive numeric string that is not greater than 1000000000"
    )
    invalid_order_type = "Invalid type is either not a string or not a valid order type"
    invalid_side_error = "Invalid side is either not a string or not a valid side"
