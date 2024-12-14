from rest_framework import serializers

from users.models import User
from users.utils import get_location_from_ip


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'role', 'is_active', 'longitude', 'latitude', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)


class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'role']

    def create(self, validated_data):
        # Get location from the IP address
        request = self.context.get('request')
        if request:
            longitude, latitude = get_location_from_ip(request)
            validated_data['longitude'] = longitude
            validated_data['latitude'] = latitude

        # Save the user with the updated location
        user = User.objects.create(**validated_data)
        return user

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        return attrs
