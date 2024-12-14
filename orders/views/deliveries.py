from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from orders.permissions import IsDeliveryUser, IsClientUser
from orders.serializers.deliveries import OrderSerializer, OrderStatusUpdateSerializer, OrderCompleteUpdateSerializer


class AllOrdersView(ListAPIView):
    """
    View to list all orders for users with the delivery role.
    """
    queryset = Order.objects.all().order_by('-created_at')  # List orders by creation date
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsDeliveryUser]
    pagination_class = PageNumberPagination


class UpdateOrderStatusView(UpdateAPIView):
    """
    View to update the status of an order to 'delivering'.
    """
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsDeliveryUser]

    def get_object(self):
        order_id = self.kwargs.get('pk')  # Get the order ID from the URL
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(detail=f"Order with ID {order_id} not found.")

    def update(self, request, *args, **kwargs):
        # Perform the update
        response = super().update(request, *args, **kwargs)
        return Response({"detail": "Order status updated to 'delivering'."})


class UpdateOrderToCompletedView(UpdateAPIView):
    """
    View to update the status of an order to 'completed'.
    """
    queryset = Order.objects.all()
    serializer_class = OrderCompleteUpdateSerializer
    permission_classes = [IsAuthenticated, IsClientUser]

    def get_object(self):
        order_id = self.kwargs.get('pk')  # Get the order ID from the URL
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(detail=f"Order with ID {order_id} not found.")

    def update(self, request, *args, **kwargs):
        # Perform the update
        response = super().update(request, *args, **kwargs)
        return Response({"detail": "Order status updated to 'completed'."})
