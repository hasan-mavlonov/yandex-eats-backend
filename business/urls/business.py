from django.urls import path, include

from business.views.business import CompanyRegisterView, BranchRegisterView, CompanyListView, CompanyDetailView

urlpatterns = [
    path('<int:user_id>/registercompany/', CompanyRegisterView.as_view(), name='company-register'),
    path('company/<int:company_id>/registerbranch/', BranchRegisterView.as_view(), name='branch-register'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('company/{company_id}/', CompanyDetailView.as_view(), name='company-detail'),
]
