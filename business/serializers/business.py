from rest_framework import serializers

from business.models import Company, Branch
from users.models import User


class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']


class BranchRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'manager_name']

    def validate_name(self, name):
        company_id = self.context['view'].kwargs.get('company_id')
        if Branch.objects.filter(name=name, company_id=company_id).exists():
            raise serializers.ValidationError('Branch with this name already exists in the company.')
        return name

    def validate_manager_name(self, manager_name):
        try:
            branch_manager = User.objects.get(name=manager_name, role='branch_manager')
        except User.DoesNotExist:
            raise serializers.ValidationError('The branch manager must exist and have the role of branch_manager.')
        return manager_name


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


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'created_by_name', 'manager_name']

    def validate(self, data):
        user = self.context.get('request').user
        if user.name != data.get('created_by_name') and user.name != data.get('manager_name'):
            raise serializers.ValidationError(
                "You are not authorized to access or modify this company."
            )

        return data
