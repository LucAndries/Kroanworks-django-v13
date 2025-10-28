"""
ADMIN.PY - V13
==============

Django admin voor rental system
Render deployment ready

Author: MiniMax Agent
Version: V13
"""

from django.contrib import admin
from .models import Rental

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """Admin interface voor Rental model"""
    list_display = ['customer_name', 'customer_email', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['customer_name', 'customer_email']
    ordering = ['-created_at']