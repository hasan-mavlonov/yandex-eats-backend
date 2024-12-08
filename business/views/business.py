from rest_framework import generics, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from business.models import Company, Branch
from business.serializers.business import CompanyRegisterSerializer, BranchRegisterSerializer, CompanySerializer
from users.models import User
from users.utils import get_location_from_ip


class CompanyRegisterView(generics.CreateAPIView):
    serializer_class = CompanyRegisterSerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        try:
            manager = User.objects.get(id=user_id, role='company_manager')
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"manager": "The provided user is not a company manager or does not exist."})

        longitude, latitude = get_location_from_ip(self.request)

        # Assign the names instead of the User objects
        serializer.save(
            created_by_name=self.request.user.name,  # Assigning name of the logged-in user
            manager_name=manager.name,  # Assigning name of the selected manager
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


class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by('created_at')  # Add ordering by created_at or another field
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # You can still filter by company_id if necessary
        company_id = self.kwargs.get('company_id')
        if company_id:
            return Company.objects.filter(id=company_id).order_by('created_at')
        return Company.objects.all().order_by('created_at')
