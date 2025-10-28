"""
PROJECT WSGI.PY - V13
=====================

WSGI configuration for Django
Render deployment ready

Author: MiniMax Agent
Version: V13
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()