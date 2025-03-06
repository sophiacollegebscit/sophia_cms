from django.urls import path
from .views import index, navbar, navbar_sidebar
from .views import about_view
from .views import syllabus_view
from .views import e_resources
from .views import placement_page
from .views import alumni_page
from .views import student_login
from .views import student_dashboard
from .views import reset_password
from .views import student_logout
from .views import timetables
from .views import student_password_reset_request, student_password_reset_confirm

urlpatterns = [
    path('', index, name='index'),
    path('navbar/', navbar, name='navbar'),
    path('navbar-sidebar/', navbar_sidebar, name='navbar_sidebar'),
    path('aboutus/', about_view, name='aboutus'),
    path("syllabus/", syllabus_view, name="syllabus"),
    path('e-resources/', e_resources, name='e_resources'),
     path("placements/", placement_page, name="placement"),
     path("alumni/", alumni_page, name="alumni"),
     path('login/', student_login, name='student_login'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('reset_password/', reset_password, name='reset_password'),
     path('logout/', student_logout, name='student_logout'),
      path("timetables/", timetables, name="timetables"),
     path("student_password_reset/", student_password_reset_request, name="student_password_reset"),
    path("reset/<str:token>/", student_password_reset_confirm, name="student_password_reset_confirm"),
]

