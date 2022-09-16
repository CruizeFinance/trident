from rest_framework import serializers


class CruizeDepositRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)


class RepayToAaveRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
