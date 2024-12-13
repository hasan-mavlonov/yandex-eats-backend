from django.urls import path

from menu.views.items import CreateFoodItemView, FoodItemListView, FoodItemDetailView

urlpatterns = [
    path('create/', CreateFoodItemView.as_view(), name='createfooditem'),
    path('fooditems/', FoodItemListView.as_view(), name='fooditems'),
    path('fooditems/<int:pk>/', FoodItemDetailView.as_view(), name='fooditem-detail'),
]
