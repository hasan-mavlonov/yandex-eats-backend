from rest_framework.permissions import BasePermission


class IsDeliveryUser(BasePermission):
    """
    Allows access only to users with the delivery role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'delivery'


class IsClientUser(BasePermission):
    """
    Allows access only to users with the delivery role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'
