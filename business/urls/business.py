from django.urls import path, include

from business.views.business import CompanyRegisterView, BranchRegisterView, CompanyListView

urlpatterns = [
    path('<int:user_id>/registercompany/', CompanyRegisterView.as_view(), name='company-register'),
    path('/company/<int:company_id>/branch/register/', BranchRegisterView.as_view(), name='branch-register'),
    path('/companies/', CompanyListView.as_view(), name='company-list'),
]
