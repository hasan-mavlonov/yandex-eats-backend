from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls.users"), name='users'),
    path('сompanies/', include("business.urls.companies"), name='companies'),
    path('branches/', include("business.urls.branches"), name='branches'),
    path('auth/', include("users.urls.auth"), name='auth'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Optional: ReDoc
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
