from rest_framework import generics, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from business.models import Branch
from menu.models import FoodItem, Menu
from menu.serializers.items import CreateFoodItemSerializer, FoodItemSerializer
from users.utils import get_location_from_ip


class CreateFoodItemView(generics.CreateAPIView):
    serializer_class = CreateFoodItemSerializer
    queryset = FoodItem.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the authenticated user is a branch manager
        if self.request.user.role != 'branch_manager':
            raise serializers.ValidationError(
                {'user': 'You must be a branch manager to perform this action.'}
            )

        # Get the menu ID from the request data
        menu_id = serializer.validated_data.get('menu').id
        try:
            # Verify that the menu belongs to a branch managed by the user
            menu = Menu.objects.get(id=menu_id, branch__manager_name=self.request.user.name)
        except Menu.DoesNotExist:
            raise serializers.ValidationError(
                {'menu': 'Invalid menu ID or you are not authorized for this menu.'}
            )

        # Save the food item with the validated menu
        serializer.save()


class FoodItemListView(generics.ListAPIView):
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class FoodItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_update(self, serializer):
        if self.request.user.role != 'branch_manager':
            raise serializers.ValidationError(
                {'user': 'You must be a branch manager to update this menu.'}
            )
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'branch_manager':
            raise serializers.ValidationError(
                {'user': 'You must be a branch manager to delete this menu.'}
            )
        instance.delete()
