from rest_framework import serializers

from business.models import Company, Branch


class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']


class BranchRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['name']

    def validate_name(self, name):
        company_id = self.context['view'].kwargs.get('company_id')
        if Branch.objects.filter(name=name, company_id=company_id).exists():
            raise serializers.ValidationError('Branch with this name already exists in the company.')
        return name
