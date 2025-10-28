"""
MODELS.PY - V13
===============

Django models voor rental system
Render deployment ready

Author: MiniMax Agent
Version: V13
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Rental(models.Model):
    """Model voor rental data"""
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_name} - {self.start_date}"
    
    class Meta:
        verbose_name = "Rental"
        verbose_name_plural = "Rentals"