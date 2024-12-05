from django.contrib import admin
from django.urls import path, include

from users import views
from users.views import UserListCreateView, UserDetailView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/', views.PhoneConfirmationView.as_view(), name='verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/resend', views.ResendPhoneVerificationView.as_view(), name='resend_phone'),
]
