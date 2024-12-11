from django.urls import path

from business.views.branches import BranchRegisterView, BranchListView, BranchDetailView

urlpatterns = [
    path('company/<int:company_id>/registerbranch/', BranchRegisterView.as_view(), name='branch-register'),
    path('branches/', BranchListView.as_view(), name='branch-list'),
    path('branch/{branch_id}/', BranchDetailView.as_view(), name='branch-detail')
]
