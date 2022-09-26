from rest_framework import serializers


class MarketDataDayRequestSerializer(serializers.Serializer):
    asset = serializers.CharField(required=True)
    vs_currency = serializers.CharField(required=False)
    days = serializers.IntegerField(required=True)


class MarketDataTimestampRequestSerializer(serializers.Serializer):
    asset = serializers.CharField(required=True)
    vs_currency = serializers.CharField(required=False)
    time_from = serializers.IntegerField(required=True)
    time_to = serializers.IntegerField(required=True)


class AssetPriceRequestSerializer(serializers.Serializer):
    asset_address = serializers.CharField(required=True)
