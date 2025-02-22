from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cms_app.urls')),  # Set cms_app as the main app
]
