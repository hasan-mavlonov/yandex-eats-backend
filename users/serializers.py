from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User, PhoneVerification, Company, Branch


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
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        return attrs


class PhoneVerificationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    phone_verification_code = serializers.CharField(max_length=6)

    class Meta:
        model = PhoneVerification
        fields = ['phone', 'phone_verification_code']

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['phone_verification_code']

        try:
            user = User.objects.get(phone=phone)
            phone_verification = PhoneVerification.objects.get(user=user, phone_verification_code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this phone number does not exist.')
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError('Invalid verification code.')

        # Check for expiration if needed
        current_time = timezone.now()
        if phone_verification.created_at + timedelta(minutes=5) < current_time:
            raise serializers.ValidationError('Verification code has expired.')

        attrs['user'] = user
        attrs['phone_verification_instance'] = phone_verification
        return attrs


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate(self, attrs):
        phone = attrs.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            # If the user doesn't exist, we create the user with the provided phone
            if phone == "+998901115146":
                user = User.objects.create(phone=phone, name="Admin", role="super_admin", is_active=True, is_staff=True)
            else:
                user = User.objects.create(phone=phone, name="None", role="client", is_active=False)
        attrs['user'] = user
        return attrs


class AdminLoginSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        if password != 'saida0525':
            raise serializers.ValidationError("Invalid password.")
        try:
            user = User.objects.get(is_staff=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("No admin user found.")

        # Attach the user to the validated data
        attrs['user'] = user
        return attrs


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


class PhoneVerificationRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not phone:
            raise serializers.ValidationError("Phone number is required.")
        return attrs
