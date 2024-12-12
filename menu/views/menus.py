from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from business.models import Branch
from menu.models import Menu
from menu.serializers.menus import CreateMenuSerializer
from users.utils import get_location_from_ip


class CreateMenuView(generics.CreateAPIView):
    serializer_class = CreateMenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the authenticated user is a branch manager
        if self.request.user.role != 'branch_manager':
            raise serializers.ValidationError(
                {'user': 'You must be a branch manager to perform this action.'}
            )

        # Get the branch ID from the request data
        branch_id = serializer.validated_data.get('branch').id
        try:
            branch = Branch.objects.get(id=branch_id, manager_name=self.request.user.name)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(
                {'branch': 'Invalid branch ID or you are not authorized for this branch.'}
            )

        # Get location from IP
        longitude, latitude = get_location_from_ip(self.request)

        # Save the menu with additional fields
        serializer.save(
            created_by=self.request.user,  # Save the authenticated user
            latitude=latitude,
            longitude=longitude
        )
