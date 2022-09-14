from rest_framework import serializers


class SlowWithdrawalSerializer(serializers.Serializer):
    position_id = serializers.IntegerField(required=True)
    amount = serializers.CharField(required=True)
    asset = serializers.CharField(required=True)
    expiration_epoch_seconds = serializers.IntegerField(required=True)
    to_address = serializers.CharField(required=True)
    user_address = serializers.CharField(required=True)


class TransferSerializer(serializers.Serializer):
    limit = serializers.CharField(required=True)
    transfer_type = serializers.CharField(required=True)


class FastWithdrawalSerializer(serializers.Serializer):
    position_id = serializers.IntegerField(required=True)
    withdrawal_amount = serializers.CharField(required=True)
    to_address = serializers.CharField(required=True)


class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
