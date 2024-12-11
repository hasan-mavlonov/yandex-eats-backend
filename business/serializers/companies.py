from rest_framework import serializers

from business.models import Company


class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'created_by_name', 'manager_name']

    def validate(self, data):
        user = self.context.get('request').user
        if user.name != data.get('created_by_name') and user.name != data.get('manager_name'):
            raise serializers.ValidationError(
                "You are not authorized to access or modify this company."
            )

        return data
