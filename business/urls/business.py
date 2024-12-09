from django.urls import path, include

from business.views.business import CompanyRegisterView, BranchRegisterView, CompanyListView, CompanyDetailView, \
    BranchListView, BranchDetailView

urlpatterns = [
    path('<int:user_id>/registercompany/', CompanyRegisterView.as_view(), name='company-register'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('company/{company_id}/', CompanyDetailView.as_view(), name='company-detail'),
    path('company/<int:company_id>/registerbranch/', BranchRegisterView.as_view(), name='branch-register'),
    path('branches/', BranchListView.as_view(), name='branch-list'),
    path('branch/{branch_id}/', BranchDetailView.as_view(), name='branch-detail'),
]