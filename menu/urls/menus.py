from django.urls import path

from menu.views.menus import CreateMenuView, MenuListCreateView, MenuDetailView

urlpatterns = [
    path('create/', CreateMenuView.as_view(), name='createmenu'),
    path('menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
]
