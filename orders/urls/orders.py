from django.urls import path

from orders.views.orders import CreateOrderView, NearestFoodItemsView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='createorder'),
    path('nearest-food-item/', NearestFoodItemsView.as_view(), name='nearest-food-item'),
]
