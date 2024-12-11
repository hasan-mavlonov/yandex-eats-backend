from rest_framework import generics, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from business.models import Branch, Company
from business.serializers.branches import BranchRegisterSerializer, BranchSerializer
from users.models import User
from users.utils import get_location_from_ip


class BranchRegisterView(generics.CreateAPIView):
    serializer_class = BranchRegisterSerializer
    queryset = Branch.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError({'company': 'Invalid company ID.'})

        # Ensure the logged-in user matches the company's manager
        if self.request.user.name != company.manager_name:
            raise serializers.ValidationError(
                {'manager': 'You are not authorized to register a branch for this company.'}
            )

        # Validate the branch manager's name
        branch_manager_name = serializer.validated_data.get('manager_name')
        try:
            branch_manager = User.objects.get(name=branch_manager_name, role='branch_manager')
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'branch_manager': 'The provided branch manager does not exist or is not a branch manager.'}
            )

        # Get location from IP
        longitude, latitude = get_location_from_ip(self.request)

        # Save the branch
        serializer.save(
            company=company,
            created_by_name=self.request.user.name,  # Logged-in user's name
            manager_name=branch_manager.name,  # Branch manager's name
            longitude=longitude,
            latitude=latitude
        )


class BranchListView(generics.ListAPIView):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all().order_by('created_at')  # Add ordering by created_at or another field
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        if branch_id:
            return Branch.objects.filter(id=branch_id).order_by('created_at')
        return Branch.objects.all().order_by('created_at')


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
    permission_classes = [IsAuthenticated]
