from rest_framework import serializers


class AmountSerializers(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
