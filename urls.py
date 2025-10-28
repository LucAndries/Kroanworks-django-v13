"""
URLS.PY - V13
=============

Main URL configuration
Render deployment ready

Author: MiniMax Agent
Version: V13
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Render deployment ready - static files handled by Django/Render