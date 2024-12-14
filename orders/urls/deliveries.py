from django.urls import path

from orders.views.deliveries import AllOrdersView, UpdateOrderStatusView, UpdateOrderToCompletedView

urlpatterns = [
    path('/allorders', AllOrdersView.as_view(), name='allorders'),
    path('/orders/<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('/orders/<int:pk>/complete/', UpdateOrderToCompletedView.as_view(), name='complete-order'),
]
