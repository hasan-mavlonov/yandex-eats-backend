import threading

from django.shortcuts import render
from rest_framework import generics, status, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Company, Branch
from users.serializers import RegisterSerializer, PhoneVerificationSerializer, LoginSerializer, \
    ResendPhoneCodeSerializer, CompanyRegisterSerializer, BranchRegisterSerializer
from users.signals import send_verification_phone
from users.utils import get_location_from_ip


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        user = serializer.save()
        longitude, latitude = get_location_from_ip(self.request)
        user.longitude = longitude
        user.latitude = latitude
        user.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = False
        user.save()
        return user


class PhoneConfirmationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneVerificationSerializer
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = validated_data.get('user')
        phone_verification_code = validated_data.get('phone_verification_instance')

        if user and phone_verification_code:
            user.is_active = True
            user.save()
            phone_verification_code.delete()

            response = {
                'success': True,
                'message': "Phone verified successfully!"
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        refresh = RefreshToken.for_user(user=serializer.validated_data['user'])
        response = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return Response(response, status=status.HTTP_200_OK)


class ResendPhoneVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendPhoneCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_thread = threading.Thread(target=send_verification_phone, args=('phone',))
        send_verification_phone(phone=serializer.validated_data['phone'])
        response = {
            'success': True,
            'message': "New code has been sent to your phone number"
        }
        return Response(response, status=status.HTTP_200_OK)


class CompanyRegisterView(generics.CreateAPIView):
    serializer_class = CompanyRegisterSerializer
    queryset = Company.objects.all()
    permission_classes = [IsAdminUser]
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
