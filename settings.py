"""
SETTINGS.PY - CLEAN VERSION V13
===========================

Django settings voor Kroanworks verhuur kalender
Render Deployment + WordPress Integration

Author: MiniMax Agent
Version: V13
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'test-secret-key-change-in-production-12345')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '127.0.0.1:8000', 
    'localhost:8000', 
    'test.kroanworks.be', 
    'roentgenologic-cormous-oscar.ngrok-free.dev',
    '*.onrender.com',  # Render deployment
    'kroanworks-django-v13.onrender.com'  # Render specific domain
]

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',  # CORS support for WordPress integration
]

LOCAL_APPS = [
    'rental_system',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware - MUST BE FIRST
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'nl-nl'
TIME_ZONE = 'Europe/Brussels'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Settings for WordPress Integration
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for development
CORS_ALLOWED_ORIGINS = [
    'https://test.kroanworks.be',
    'https://roentgenologic-cormous-oscar.ngrok-free.dev',
]

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'rental_system': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# ========================================
# KROANWORKS VERHUUR CONFIGURATION
# ========================================

# WordPress Integration Settings
WORDPRESS_API_URL = os.environ.get('WORDPRESS_API_URL', 'https://test.kroanworks.be/wp-json')
WORDPRESS_JWT_USERNAME = os.environ.get('WORDPRESS_JWT_USERNAME', 'Luc_Snel')
WORDPRESS_JWT_PASSWORD = os.environ.get('WORDPRESS_JWT_PASSWORD', 'Mozart-480111')
WORDPRESS_HOME_URL = os.environ.get('WORDPRESS_HOME_URL', 'https://test.kroanworks.be/home')

# Rental System Settings
EXTRA_KM_TARIFF = float(os.environ.get('EXTRA_KM_TARIFF', '0.30'))
VOORSCHOT_PERCENTAGE = int(os.environ.get('VOORSCHOT_PERCENTAGE', '30'))
PREPAIEMENT_TYPE = os.environ.get('PREPAIEMENT_TYPE', 'huur_borg')  # 'huur_borg' or 'huur_alleen'
VOORBEHOUDEN_DAGEN = os.environ.get('VOORBEHOUDEN_DAGEN', '["2025-12-25", "2025-12-26"]')

# Convert VOORBEHOUDEN_DAGEN from string to list
try:
    import json
    VOORBEHOUDEN_DAGEN = json.loads(VOORBEHOUDEN_DAGEN)
except:
    VOORBEHOUDEN_DAGEN = ['2025-12-25', '2025-12-26']

# Calendar Settings
CALENDAR_HEIGHT = os.environ.get('CALENDAR_HEIGHT', '700px')
CALENDAR_WIDTH = os.environ.get('CALENDAR_WIDTH', '100%')
CALENDAR_DEFAULT_VIEW = os.environ.get('CALENDAR_DEFAULT_VIEW', 'dayGridMonth')

# Price Calculation Settings
DEFAULT_DEPOSIT = float(os.environ.get('DEFAULT_DEPOSIT', '100.00'))
MIN_RENTAL_DAYS = int(os.environ.get('MIN_RENTAL_DAYS', '1'))
MAX_RENTAL_DAYS = int(os.environ.get('MAX_RENTAL_DAYS', '30'))

# Email Settings (for notifications)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Use 'smtp' in production
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@kroanworks.be')

# Security Settings for Production
SECURE_BROWSER_XSS_FILTER = os.environ.get('SECURE_BROWSER_XSS_FILTER', 'True').lower() in ['true', 'on', '1']
SECURE_CONTENT_TYPE_NOSNIFF = os.environ.get('SECURE_CONTENT_TYPE_NOSNIFF', 'True').lower() in ['true', 'on', '1']
X_FRAME_OPTIONS = 'ALLOWALL'  # Allow iframe embedding for WordPress

# Session Settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS

# CSRF Settings
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS

# CSRF trusted origins for ngrok and Render
CSRF_TRUSTED_ORIGINS = [
    'https://roentgenologic-cormous-oscar.ngrok-free.dev',
    'https://*.onrender.com',
    'https://kroanworks-django-v13.onrender.com',
]

# ngrok public URL for reference
NGROK_PUBLIC_URL = 'https://roentgenologic-cormous-oscar.ngrok-free.dev'

# Cache Settings (optional)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# ========================================
# WORDPRESS API HELPER FUNCTIONS
# ========================================

def get_rental_context():
    """Get rental system context for templates"""
    return {
        'wordpress_api_url': WORDPRESS_API_URL,
        'wordpress_home_url': WORDPRESS_HOME_URL,
        'extra_km_tariff': EXTRA_KM_TARIFF,
        'voorschot_percentage': VOORSCHOT_PERCENTAGE,
        'prepaiement_type': PREPAIEMENT_TYPE,
        'voorbedeouden_dagen': VOORBEHOUDEN_DAGEN,
        'calendar_height': CALENDAR_HEIGHT,
        'calendar_width': CALENDAR_WIDTH,
    }

def is_wordpress_available():
    """Check if WordPress API is available"""
    try:
        import requests
        response = requests.get(f"{WORDPRESS_API_URL}/wp/v2/posts", timeout=5)
        return response.status_code == 200
    except:
        return False

# ========================================
# DEVELOPMENT SETTINGS OVERRIDE
# ========================================

if DEBUG:
    # Development specific settings
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]
    
    # Add debug toolbar in development
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1']
    except ImportError:
        pass
    
    # Allow all hosts in development
    ALLOWED_HOSTS = ['*']
    
    # More permissive CORS settings for development
    CORS_ALLOW_ALL_ORIGINS = True

# ========================================
# RENDER DEPLOYMENT CHECKLIST
# ========================================

# ✅ Render deployment requirements met:
# - CORS middleware configured
# - ALLOWED_HOSTS includes *.onrender.com  
# - CSRF_TRUSTED_ORIGINS includes Render domains
# - Environment variables configured
# - Gunicorn ready
# - WordPress integration enabled

# TODO: Before production deployment, update:
# - SECRET_KEY (generate new via djecrety.ir)
# - DEBUG = False
# - WordPress credentials
# - Database (PostgreSQL recommended)
# - SSL certificate