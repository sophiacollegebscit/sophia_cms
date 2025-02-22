from django.urls import path
from .views import index, navbar, navbar_sidebar

urlpatterns = [
    path('', index, name='index'),
    path('navbar/', navbar, name='navbar'),
    path('navbar-sidebar/', navbar_sidebar, name='navbar_sidebar'),
]

