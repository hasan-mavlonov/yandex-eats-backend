from rest_framework import serializers

from menu.models import Menu


class CreateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ['created_by', 'latitude', 'longitude']  # Exclude fields managed by the view
