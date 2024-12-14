from rest_framework import serializers

from business.models import Branch
from menu.models import Menu, FoodItem
from orders.models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    food_item_id = serializers.IntegerField()  # The ID of the food item being ordered
    quantity = serializers.IntegerField(min_value=1)  # Must be at least 1

    def validate_food_item_id(self, value):
        # Validate that the food item exists and is available
        if not FoodItem.objects.filter(id=value, available=True).exists():
            raise serializers.ValidationError(f"Invalid or unavailable food item ID: {value}")
        return value


class OrderCreateSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()  # The ID of the menu
    items = OrderItemCreateSerializer(many=True)  # List of items being ordered

    def validate_menu_id(self, value):
        # Check if the menu exists
        if not Menu.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid menu ID.")
        return value

    def create(self, validated_data):
        menu_id = validated_data['menu_id']
        items_data = validated_data['items']

        # Get the menu and branch
        menu = Menu.objects.get(id=menu_id)
        branch = menu.branch

        # Create the order
        order = Order.objects.create(
            client=self.context['request'].user,  # Assumes user is authenticated
            branch=branch,
            latitude=self.context['request'].user.latitude,
            longitude=self.context['request'].user.longitude,
        )

        # Create order items
        for item in items_data:
            food_item = FoodItem.objects.get(id=item['food_item_id'])
            if food_item.menu.id != menu_id:
                raise serializers.ValidationError(
                    f"Food item {food_item.name} does not belong to the selected menu."
                )
            OrderItem.objects.create(
                order=order,
                menu=menu,
                quantity=item['quantity'],
                price=food_item.price * item['quantity'],
            )

        order.status = 'pending'
        order.save()

        return order

    def to_representation(self, instance):
        # Customize output representation
        return {
            'id': instance.id,
            'client': instance.client.id,
            'branch': instance.branch.id,
            'status': instance.status,
            'latitude': float(instance.latitude),
            'longitude': float(instance.longitude),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }


