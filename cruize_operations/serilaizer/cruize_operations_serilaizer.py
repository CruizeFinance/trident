from rest_framework import serializers


class CruizeDepositRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    asset_address = serializers.CharField(required=True)


class RepayToAaveRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)


class FirebaeRequestSerializer(serializers.Serializer):
    user_address = serializers.CharField(
        required=True,
        min_length=42,
    )  # id will be user wallet address.
    transaction_hash = serializers.CharField(required=True)
    asset_name = serializers.CharField(required=True)
    amount = serializers.CharField(required=True)
    type = serializers.CharField(required=True)


class FirebaseFecthRequestSerializer(serializers.Serializer):
    user_address = serializers.CharField(
        required=True, min_length=42
    )  # id will be user wallet address.


class PriceFloorSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=True)
    days = serializers.CharField(required=True)
