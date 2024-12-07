from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from users.urls import business

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls.users"), name='users'),
    path('business/', include("users.urls.business"), name='business'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Optional: ReDoc
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
