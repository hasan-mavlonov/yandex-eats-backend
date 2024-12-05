from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, max_length=120)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'role', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Passwords must match.')
        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return attrs


class PhoneVerificationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone')
    phone_verification_code = serializers.CharField(max_length=6)

    class Meta:
        model = PhoneVerification
        fields = ['phone', 'phone_verification_code']

    def validate(self, attrs):
        phone = attrs['user']['phone']
        code = attrs['phone_verification_code']

        try:
            user = User.objects.get(phone=phone)
            phone_verification = PhoneVerification.objects.get(user=user, phone_verification_code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this phone number does not exist.')
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError('Invalid phone verification code.')

        # Check if the code has expired
        current_time = timezone.now()
        if phone_verification.created_at + timedelta(minutes=2) < current_time:
            phone_verification.delete()  # Optionally delete expired codes
            raise serializers.ValidationError('Phone verification code has expired.')

        attrs['user'] = user
        attrs['phone_verification_instance'] = phone_verification
        return attrs


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    error_message = "Invalid Credentials"

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(self.error_message)
        authenticated_user = authenticate(request=self.context.get('request'), phone=phone, password=password)
        if not authenticated_user:
            raise serializers.ValidationError(self.error_message)
        attrs['user'] = authenticated_user
        return attrs


class ResendPhoneCodeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this phone number does not exist.')
        attrs['user'] = user
        return attrs

    class Meta:
        model = PhoneVerification
        fields = ['phone']


class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', la]


class BranchRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['name']

    def validate_name(self, name):
        company_id = self.context['view'].kwargs.get('company_id')
        if Branch.objects.filter(name=name, company_id=company_id).exists():
            raise serializers.ValidationError('Branch with this name already exists in the company.')
        return name
