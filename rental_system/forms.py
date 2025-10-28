"""
FORMS.PY - V13
==============

Django forms voor rental system
Render deployment ready

Author: MiniMax Agent
Version: V13
"""

from django import forms
from .models import Rental

class RentalForm(forms.ModelForm):
    """Form voor rental data"""
    
    class Meta:
        model = Rental
        fields = ['customer_name', 'customer_email', 'start_date', 'end_date']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }