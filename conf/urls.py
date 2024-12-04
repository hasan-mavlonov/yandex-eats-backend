from django.contrib import admin
from django.urls import path, include

from users.urls import business

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls.users"), name='users'),
    path('business/', include("users.urls.business"), name='business'),
]
