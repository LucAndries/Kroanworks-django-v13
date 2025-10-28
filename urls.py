"""
URLS.PY - V13
=============
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rental_system.urls')),  # ← Dit is de fix
]

