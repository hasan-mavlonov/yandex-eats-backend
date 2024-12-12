from django.urls import path
from business.views.companies import CompanyRegisterView, CompanyListView, CompanyDetailView

urlpatterns = [
    path('<int:user_id>/registercompany/', CompanyRegisterView.as_view(), name='business-company-register'),
    path('', CompanyListView.as_view(), name='business-company-list'),
    path('<int:company_id>/', CompanyDetailView.as_view(), name='business-company-detail'),
]
