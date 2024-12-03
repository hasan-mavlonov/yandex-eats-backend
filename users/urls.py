from django.contrib import admin
from django.urls import path, include

from users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/', views.PhoneConfirmationView.as_view(), name='verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/phone/resend', views.ResendPhoneVerificationView.as_view(), name='resend_phone'),
]
