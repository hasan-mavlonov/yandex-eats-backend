from django.urls import path

from business.views.companies import CompanyRegisterView, CompanyListView, CompanyDetailView

urlpatterns = [
    path('<int:user_id>/registercompany/', CompanyRegisterView.as_view(), name='company-register'),
    path('companies.py/', CompanyListView.as_view(), name='company-list'),
    path('company/{company_id}/', CompanyDetailView.as_view(), name='company-detail')
]
