from rest_framework import serializers


class slowWithdrawalSerializer(serializers.Serializer):
    position_id = serializers.IntegerField(required=True)
    amount = serializers.CharField(required=True)
    asset = serializers.CharField(required=True)
    expiration_epoch_seconds = serializers.IntegerField(required=True)
    to_address = serializers.CharField(required=True)


class transferSerializer(serializers.Serializer):
    limit = serializers.CharField(required=True)
    transfer_type = serializers.CharField(required=True)


class fastWithdrawalSerializer(serializers.Serializer):
    position_id = serializers.IntegerField(required=True)
    credit_asset = serializers.CharField(required=True)
    credit_amount = serializers.CharField(required=True)
    debit_amount = serializers.CharField(required=True)
    to_address = serializers.CharField(required=True)
    lp_position_id = serializers.CharField(required=True)
    expiration_epoch_seconds = serializers.CharField(required=True)
    signature = serializers.CharField(required=True)
