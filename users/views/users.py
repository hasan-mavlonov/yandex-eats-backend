from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.models import User
from users.pagination import UserPagination
from users.serializers.users import AddUserSerializer, UserSerializer
from users.utils import get_location_from_ip


class AddUserView(generics.CreateAPIView):
    serializer_class = AddUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        user = serializer.save()
        user.save()
        user.is_active = True
        user.save()
        return user


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
