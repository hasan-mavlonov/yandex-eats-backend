from rest_framework import generics, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from business.models import Company, Branch
from business.serializers.business import CompanyRegisterSerializer, BranchRegisterSerializer
from users.utils import get_location_from_ip


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
