from rest_framework import serializers

from menu.models import FoodItem


class CreateFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        exclude = ['created_at', 'updated_at']  # Exclude fields automatically managed by Django


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'  # Include all fields
