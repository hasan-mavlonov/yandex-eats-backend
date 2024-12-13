from django.urls import path

from menu.views.items import CreateFoodItemView

urlpatterns = [
    path('create/', CreateFoodItemView.as_view(), name='createfooditem'),
]
