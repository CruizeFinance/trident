from rest_framework import serializers

class AssetPriceRequestSerializer(serializers.Serializer):
    asset_name = serializers.CharField(required=True)
