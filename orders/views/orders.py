from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import F, FloatField
from django.db.models.functions import Sqrt, Power
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from menu.models import FoodItem, Menu
from menu.serializers.items import FoodItemSerializer
from orders.serializers.orders import OrderCreateSerializer


class CreateOrderView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class NearestFoodItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Ensure the user has a valid location
        if not user.latitude or not user.longitude:
            return Response({"error": "User location not set."}, status=400)

        # Calculate distance to menus
        menus = Menu.objects.annotate(
            distance=Sqrt(
                Power(F('latitude') - user.latitude, 2) +
                Power(F('longitude') - user.longitude, 2)
            )
        ).order_by('distance')

        # Fetch food items from menus ordered by proximity
        nearest_food_items = FoodItem.objects.filter(
            menu__in=menus, available=True
        ).select_related('menu')

        # Serialize the data
        serializer = FoodItemSerializer(nearest_food_items, many=True)
        return Response(serializer.data)
