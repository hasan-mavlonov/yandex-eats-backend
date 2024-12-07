
from django.urls import path

from users.views.users import UserDetailView, UserListCreateView, AddUserView
urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('admin/adduser/', AddUserView.as_view(), name='register'),
]
