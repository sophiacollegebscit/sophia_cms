from django.urls import path
from .views import index, navbar, navbar_sidebar
from .views import about_view
from .views import syllabus_view
from .views import e_resources
from .views import placement_page

urlpatterns = [
    path('', index, name='index'),
    path('navbar/', navbar, name='navbar'),
    path('navbar-sidebar/', navbar_sidebar, name='navbar_sidebar'),
    path('aboutus/', about_view, name='aboutus'),
    path("syllabus/", syllabus_view, name="syllabus"),
    path('e-resources/', e_resources, name='e_resources'),
     path("placements/", placement_page, name="placement"),
]

