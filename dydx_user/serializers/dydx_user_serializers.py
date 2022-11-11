from rest_framework import serializers


class PositionidSerializers(serializers.Serializer):
    asset_pair = serializers.CharField(required=True)


class RegisterUserSerializers(serializers.Serializer):
    asset_pair = serializers.CharField(required=True)
