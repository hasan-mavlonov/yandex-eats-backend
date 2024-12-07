from django.urls import path, include

from users.views import CompanyRegisterView, BranchRegisterView

urlpatterns = [
    path('company/register/', CompanyRegisterView.as_view(), name='company-register'),
    path('/company/<int:company_id>/branch/register/', BranchRegisterView.as_view(), name='branch-register'),
]
