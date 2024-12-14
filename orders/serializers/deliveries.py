from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'client',
            'branch',
            'status',
            'latitude',
            'longitude',
            'created_at',
            'updated_at',
        ]


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']  # Only allow updating the status field

    def validate_status(self, value):
        if value != 'delivering':
            raise serializers.ValidationError("Status can only be updated to 'delivering'.")
        return value


class OrderCompleteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']  # Only allow updating the status field

    def validate_status(self, value):
        if value != 'completed':
            raise serializers.ValidationError("Status can only be updated to 'completed'.")
        return value

    def validate(self, attrs):
        order = self.instance  # Access the order instance being updated
        if order.status != 'delivering':
            raise serializers.ValidationError("Order status can only be updated to 'completed' from 'delivering'.")
        return attrs
