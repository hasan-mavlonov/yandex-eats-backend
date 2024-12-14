from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from menu.urls import items

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls.users"), name='users'),
    path('companies/', include("business.urls.companies"), name='companies'),
    path('branches/', include("business.urls.branches"), name='branches'),
    path('menus/', include("menu.urls.menus"), name='menus'),
    path('items/', include("menu.urls.items"), name='items'),
    path('orders/', include("orders.urls.orders"), name='orders'),
    path('auth/', include("users.urls.auth"), name='auth'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
