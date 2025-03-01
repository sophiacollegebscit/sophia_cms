from django.urls import path
from .views import index, navbar, navbar_sidebar
from .views import about_view
from .views import syllabi_view
from .views import e_resources

urlpatterns = [
    path('', index, name='index'),
    path('navbar/', navbar, name='navbar'),
    path('navbar-sidebar/', navbar_sidebar, name='navbar_sidebar'),
    path('aboutus/', about_view, name='aboutus'),
    path('syllabi/', syllabi_view, name="syllabi"),
    path('e-resources/', e_resources, name='e_resources'),
]

