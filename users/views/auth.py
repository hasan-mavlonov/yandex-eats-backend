from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers.auth import LoginSerializer, AdminLoginSerializer, PhoneVerificationSerializer, \
    PhoneVerificationRequestSerializer

from users.signals import send_verification_code

from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginView(APIView):
    serializer_class = LoginSerializer
    http_method_names = ['get', 'post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        user = serializer.validated_data['user']

        if user.is_staff or user.is_superuser:
            return HttpResponseRedirect(reverse('admin-login'))  # Redirect to Admin Login view

        if not user.is_active:
            return HttpResponseRedirect(reverse('send-phone-verification-code'))  # Redirect for phone verification

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'message': f'{user.get_role_display()} logged in successfully!',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)


class AdminLoginView(APIView):
    serializer_class = AdminLoginSerializer
    http_method_names = ['get', 'post']
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user from validated data
        user = serializer.validated_data['user']

        # Generate the refresh and access tokens for the authenticated admin user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return the response with the tokens
        return Response({
            'message': 'Admin logged in successfully!',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)


class PhoneVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneVerificationSerializer
    http_method_names = ['get', 'post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        phone_verification_code = serializer.validated_data.get('phone_verification_instance')

        # If user and phone verification code are valid
        if user and phone_verification_code:
            # Activate user after verification
            user.is_active = True
            user.save()

            # Delete the phone verification instance (optional)
            phone_verification_code.delete()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'message': 'Phone verified successfully!',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data or code"}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import redirect


class SendPhoneVerificationCodeView(APIView):
    http_method_names = ['get', 'post']

    def get(self, request):
        return Response({'message': 'Send a POST request with the phone number to receive a verification code.'},
                        status=status.HTTP_200_OK)

    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'User with this phone number does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Send the verification code via SMS
            send_verification_code(phone)
        except Exception as e:
            return Response({'error': f'Failed to send verification code: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Redirect to the 'verify-phone' view
        return redirect('verify-phone')  # Django shortcut for HttpResponseRedirect(resolve_url(...))
