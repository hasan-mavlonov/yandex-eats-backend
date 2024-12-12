from django.urls import path

from menu.views.menus import CreateMenuView

urlpatterns = [
    path('create/', CreateMenuView.as_view(), name='createmenu'),
]
