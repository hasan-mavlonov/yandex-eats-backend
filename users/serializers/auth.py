from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import serializers

from users.models import User, PhoneVerification
from users.utils import get_location_from_ip


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
            if phone == "+998901115146":
                user = User.objects.create(
                    phone=phone,
                    name="Admin",
                    role="super_admin",
                    is_active=True,
                    is_staff=True,
                    is_superuser=True
                )
            else:
                longitude, latitude = get_location_from_ip(self.context.get('request'))
                user = User.objects.create(phone=phone, name="None", role="client", is_active=False,
                                           longitude=longitude, latitude=latitude)
        attrs['user'] = user
        return attrs


class AdminLoginSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        if password != 'saida0525':
            raise serializers.ValidationError("Invalid password.")

        try:
            user = User.objects.get(phone="+998901115146")  # Ensure this is the correct admin user
        except User.DoesNotExist:
            raise serializers.ValidationError("Admin user not found.")

        # Hash the password before saving
        user.password = make_password(password)  # Save the hashed password
        user.save()

        # Attach the user to the validated data
        attrs['user'] = user
        return attrs


class PhoneVerificationRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not phone:
            raise serializers.ValidationError("Phone number is required.")
        return attrs
