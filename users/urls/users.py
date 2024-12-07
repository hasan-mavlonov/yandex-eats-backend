from django.contrib import admin
from django.urls import path, include

from users import views
from users.views import UserListCreateView, UserDetailView, SendPhoneVerificationCodeView, PhoneVerificationView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('admin/adduser/', views.AddUserView.as_view(), name='register'),
    path('send-phone-verification-code/', SendPhoneVerificationCodeView.as_view(), name='send-phone-verification-code'),
    path('verify-phone/', PhoneVerificationView.as_view(), name='verify-phone'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('admin/login', views.AdminLoginView.as_view(), name='admin-login'),
]
