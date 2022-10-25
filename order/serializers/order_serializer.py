from rest_framework import serializers


class OrderRequestSerializer(serializers.Serializer):
    market = serializers.CharField(required=True)
    side = serializers.CharField(max_length=4, required=True)
    size = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)

    def validate(self, data):
        if not data["market"].isupper() or not data["side"].isupper():
            raise serializers.ValidationError(
                "please make sure you use all Capital letters for market ,side and order_type"
            )
        return data


class CancelOrderRequestSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True)


class FirestoreOrdersRequestSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=False)
