from rest_framework import serializers


class CruizeDepositRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    asset_address = serializers.CharField(required=True)


class RepayToAaveRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
