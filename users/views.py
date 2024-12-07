import threading
from datetime import timedelta

from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework import generics, status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Company, Branch, PhoneVerification
from users.pagination import UserPagination
from users.serializers import PhoneVerificationSerializer, LoginSerializer, CompanyRegisterSerializer, \
    BranchRegisterSerializer, UserSerializer, AddUserSerializer, \
    PhoneVerificationRequestSerializer, AdminLoginSerializer
from users.signals import send_verification_phone, send_verification_code
from users.utils import get_location_from_ip


class AddUserView(generics.CreateAPIView):
    serializer_class = AddUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        user = serializer.save()
        user.save()
        user.is_active = False
        user.save()
        return user


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        user = serializer.validated_data['user']
        if user.is_staff or user.is_superuser:
            return redirect('admin-login')
        if not user.is_active:
            return redirect('send-phone-verification-code')
        else:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

        return Response({
            'message': 'User logged in successfully!',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)


class AdminLoginView(APIView):
    serializer_class = AdminLoginSerializer

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


class CompanyRegisterView(generics.CreateAPIView):
    serializer_class = CompanyRegisterSerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        longitude, latitude = get_location_from_ip(self.request)
        serializer.save(
            created_by=self.request.user,
            longitude=longitude,
            latitude=latitude
        )


class BranchRegisterView(generics.CreateAPIView):
    serializer_class = BranchRegisterSerializer
    queryset = Branch.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError({'company': 'Invalid company ID.'})

        longitude, latitude = get_location_from_ip(self.request)
        serializer.save(
            company=company,
            created_by=self.request.user,
            longitude=longitude,
            latitude=latitude
        )


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination

    def get_queryset(self):
        # Optionally filter users based on query parameters
        role = self.request.query_params.get('role', None)
        if role:
            return self.queryset.filter(role=role)
        return self.queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination

    def perform_update(self, serializer):
        serializer.save()


class PhoneVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneVerificationSerializer

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


class SendPhoneVerificationCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneVerificationRequestSerializer

    def post(self, request):
        phone = request.data.get('phone')

        if not phone:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'User with this phone number does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Send the verification code via SMS
        send_verification_code(phone)

        return Response({'message': 'Verification code sent successfully! Please check your phone.'},
                        status=status.HTTP_200_OK)
