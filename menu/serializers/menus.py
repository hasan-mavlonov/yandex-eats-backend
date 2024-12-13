from rest_framework import serializers

from menu.models import Menu


class CreateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ['created_by', 'latitude', 'longitude']  # Exclude fields managed by the view


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'  # Include all fields for CRUD operations
        read_only_fields = ['created_by', 'latitude', 'longitude', 'created_at', 'updated_at']
