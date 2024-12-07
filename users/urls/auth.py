from django.urls import path

from users.views.auth import SendPhoneVerificationCodeView, PhoneVerificationView, AdminLoginView, LoginView

urlpatterns = [
    path('send-phone-verification-code/', SendPhoneVerificationCodeView.as_view(), name='send-phone-verification-code'),
    path('verify-phone/', PhoneVerificationView.as_view(), name='verify-phone'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/login', AdminLoginView.as_view(), name='admin-login'),
]
