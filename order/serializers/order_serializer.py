from rest_framework import serializers


class OrderRequestSerializer(serializers.Serializer):
    position_id = serializers.IntegerField(
        required=True,
        min_value=0,
    )
    market = serializers.CharField(required=True)
    side = serializers.CharField(max_length=4, required=True)
    order_type = serializers.CharField(max_length=6, required=True)
    post_only = serializers.BooleanField(required=True)
    size = serializers.CharField(required=True)
    price = serializers.CharField(required=True)
    limit_fee = serializers.FloatField(required=True, min_value=0)
    expiration_epoch_seconds = serializers.IntegerField(required=True)
    time_in_force = serializers.CharField(required=True)
    trailing_percent = serializers.CharField(required=True)
    trigger_price = serializers.CharField(required=True)

    def validate(self, data):
        if (
            not data["market"].isupper()
            or not data["side"].isupper()
            or not data["order_type"].isupper()
        ):
            raise serializers.ValidationError(
                "please make sure you use all Capital letters for market ,side and order_type"
            )
        return data


class CancelOrderRequestSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True)


class FirestoreOrdersRequestSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=False)
