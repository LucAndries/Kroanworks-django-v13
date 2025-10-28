"""
APPS.PY - V13
=============

Django app configuration
Render deployment ready

Author: MiniMax Agent
Version: V13
"""

from django.apps import AppConfig

class RentalSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental_system'
    verbose_name = 'Rental System V13'
    
    def ready(self):
        pass