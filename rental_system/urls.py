"""
RENTAL SYSTEM URLS.PY - V13
============================

Rental system URL configuration
Render deployment ready

Author: MiniMax Agent
Version: V13
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main views
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/health', views.api_health, name='api_health'),
    path('api/user-session', views.api_user_session, name='api_user_session'),
    path('api/availability', views.api_availability, name='api_availability'),
    path('api/calculate-price', views.api_calculate_price, name='api_calculate_price'),
    path('api/create-reservation', views.api_create_reservation, name='api_create_reservation'),
    path('api/login', views.api_login, name='api_login'),
    path('api/logout', views.api_logout, name='api_logout'),
    path('api/status', views.api_status, name='api_status'),
    path('api/wordpress-test', views.api_wordpress_test, name='api_wordpress_test'),
    
    # Additional API endpoints
    path('api/formulas', views.api_formulas, name='api_formulas'),
    path('api/debug-formulas', views.api_debug_formulas, name='api_debug_formulas'),
    path('api/info', views.api_info, name='api_info'),
]