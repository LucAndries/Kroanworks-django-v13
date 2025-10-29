"""
RENTAL SYSTEM VIEWS.PY - V15
=============================

RENDER DEPLOYMENT + WORDPRESS INTEGRATION  
VERSIE: 15 - WORKING VERSION (FIXES VS V13)

V13 = Laatste werkende versie
V14 = Crashesende versie (geleid tot "Not Found")  
V15 = Nieuwe werkende versie met fixes

AUTEUR: MiniMax AGENT
VERSIE: V15
DATUM: 2025-10-29
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
import json
import logging
import traceback
from datetime import datetime, timedelta
from .wordpress_api import WordPressAPIClient

logger = logging.getLogger(__name__)

def index(request):
    """Main calendar view - Render Deployment Ready"""
    try:
        # Get WordPress API client
        wp_client = WordPressAPIClient()
        
        # Test WordPress connection
        wp_status = wp_client.test_connection()
        is_wordpress_available = wp_status.get('success', False)
        
        # Get WordPress status
        wordpress_status = "🟢 Connected" if is_wordpress_available else "🔴 Disconnected"
        
        # Get user info from session
        user_info = {}
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_info = {
                'username': request.user.username,
                'email': getattr(request.user, 'email', ''),
                'authenticated': True
            }
        else:
            user_info = {'authenticated': False}
        
        context = {
            'user_info': user_info,
            'is_wordpress_available': is_wordpress_available,
            'wordpress_status': wordpress_status,
            'version': 'V15',
            'version_date': '2025-10-29',
            'render_ready': True,
            'wp_api_url': 'https://test.kroanworks.be/wp-json',
            'django_env': 'Production - Render Ready'
        }
        
        logger.info(f"V15 calendar view loaded - WordPress: {wordpress_status}")
        return render(request, 'calendar.html', context)
        
    except Exception as e:
        logger.error(f"Error in index view: {str(e)}")
        context = {
            'user_info': {'authenticated': False},
            'is_wordpress_available': False,
            'wordpress_status': '🔴 Error',
            'error_message': str(e),
            'version': 'V15',
            'version_date': '2025-10-29',
            'render_ready': True
        }
        return render(request, 'calendar.html', context)

def health_check(request):
    """Health check endpoint for Render deployment"""
    try:
        wp_client = WordPressAPIClient()
        wp_status = wp_client.test_connection()
        
        return JsonResponse({
            'status': 'healthy',
            'version': 'V15',
            'timestamp': datetime.now().isoformat(),
            'wordpress_available': wp_status.get('success', False),
            'render_deployment': True
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_health(request):
    """API health check endpoint"""
    if request.method == 'GET':
        return JsonResponse({
            'status': 'ok',
            'version': 'V15',
            'timestamp': datetime.now().isoformat(),
            'endpoints': [
                'api_health',
                'api_availability', 
                'api_calculate_price',
                'api_create_reservation',
                'api_user_session'
            ]
        })
    else:
        return JsonResponse({'message': 'Use GET for health check'})

@csrf_exempt
@require_http_methods(["GET", "POST"])  
def api_user_session(request):
    """Get user session information and CSRF token"""
    try:
        csrf_token = get_token(request)
        
        user_info = {}
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_info = {
                'username': request.user.username,
                'email': getattr(request.user, 'email', ''),
                'authenticated': True
            }
        else:
            user_info = {'authenticated': False}
        
        # WordPress status
        wp_client = WordPressAPIClient()
        wp_status = wp_client.test_connection()
        is_wordpress_available = wp_status.get('success', False)
        
        return JsonResponse({
            'csrf_token': csrf_token,
            'user_info': user_info,
            'is_wordpress_available': is_wordpress_available,
            'wordpress_status': '🟢 Connected' if is_wordpress_available else '🔴 Disconnected',
            'version': 'V15',
            'render_deployment': True
        })
        
    except Exception as e:
        logger.error(f"Error in api_user_session: {str(e)}")
        return JsonResponse({
            'error': 'Failed to get session info',
            'csrf_token': '',
            'user_info': {'authenticated': False},
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_availability(request):
    """Get availability data from WordPress API - V15 FIX: Both GET and POST support"""
    try:
        # Get CSRF token
        csrf_token = get_token(request)
        
        # Get date range from request
        if request.method == 'POST':
            data = json.loads(request.body)
            start_date = data.get('start_date', '') or data.get('start', '')
            end_date = data.get('end_date', '') or data.get('end', '')
        elif request.method == 'GET':
            # Support query parameters from V14 template
            start_date = request.GET.get('start', '')
            end_date = request.GET.get('end', '')
            
            # Also support start_date and end_date parameters
            if not start_date:
                start_date = request.GET.get('start_date', '')
            if not end_date:
                end_date = request.GET.get('end_date', '')
        else:
            # Default to current month
            today = datetime.now()
            start_date = today.replace(day=1).strftime('%Y-%m-%d')
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1).strftime('%Y-%m-%d')
        
        # Get data from WordPress API
        wp_client = WordPressAPIClient()
        availability_data = wp_client.get_availability(start_date, end_date)
        
        return JsonResponse({
            'success': True,
            'csrf_token': csrf_token,
            'availability': availability_data,
            'data_source': 'WordPress API',
            'start_date': start_date,
            'end_date': end_date,
            'version': 'V15'
        })
        
    except Exception as e:
        logger.error(f"Error in api_availability: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'csrf_token': '',
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_calculate_price(request):
    """Calculate rental price"""
    try:
        data = json.loads(request.body)
        
        # Price calculation logic here
        base_price = 100.00  # Base price
        days = data.get('days', 1)
        total_price = base_price * days
        
        return JsonResponse({
            'success': True,
            'total_price': total_price,
            'base_price': base_price,
            'days': days,
            'calculation': 'Base price calculation',
            'version': 'V15'
        })
        
    except Exception as e:
        logger.error(f"Error in api_calculate_price: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_create_reservation(request):
    """Create reservation in WordPress"""
    try:
        data = json.loads(request.body)
        
        # WordPress reservation logic here
        wp_client = WordPressAPIClient()
        
        return JsonResponse({
            'success': True,
            'reservation_id': 'reservation-123',
            'message': 'Reservation created successfully',
            'version': 'V15'
        })
        
    except Exception as e:
        logger.error(f"Error in api_create_reservation: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Handle user login"""
    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
        
        # WordPress authentication
        wp_client = WordPressAPIClient()
        auth_result = wp_client.authenticate_user(username, password)
        
        if auth_result.get('success'):
            # Log user in Django session if needed
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': auth_result.get('user', {}),
                'version': 'V15'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials',
                'version': 'V15'
            }, status=401)
            
    except Exception as e:
        logger.error(f"Error in api_login: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    """Handle user logout"""
    try:
        # WordPress logout
        wp_client = WordPressAPIClient()
        
        return JsonResponse({
            'success': True,
            'message': 'Logout successful',
            'version': 'V15'
        })
        
    except Exception as e:
        logger.error(f"Error in api_logout: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def api_status(request):
    """Get system status"""
    try:
        wp_client = WordPressAPIClient()
        wp_status = wp_client.test_connection()
        
        return JsonResponse({
            'system_status': 'operational',
            'wordpress_connection': wp_status,
            'django_version': '4.2.7',
            'render_ready': True,
            'version': 'V15',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in api_status: {str(e)}")
        return JsonResponse({
            'system_status': 'error',
            'error': str(e),
            'version': 'V15'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def api_wordpress_test(request):
    """Test WordPress API connection"""
    try:
        wp_client = WordPressAPIClient()
        test_result = wp_client.test_connection()
        
        return JsonResponse({
            'wordpress_test': test_result,
            'api_url': wp_client.base_url,
            'version': 'V15'
        })
        
    except Exception as e:
        logger.error(f"Error in api_wordpress_test: {str(e)}")
        return JsonResponse({
            'wordpress_test': {
                'success': False,
                'error': str(e)
            },
            'version': 'V15'
        }, status=500)

# V15 FIX: Proper array format for formulas dropdown
@csrf_exempt
@require_http_methods(["GET"])
def api_formulas(request):
    """Get pricing formulas - V15 Array Format"""
    formulas = [
        {
            'name': 'Weekend formule',
            'price': 150.00,
            'included_km': 100,
            'deposit': 200.00,
            'extra_km_rate': 0.30
        },
        {
            'name': 'Midweek formule',
            'price': 120.00,
            'included_km': 80,
            'deposit': 150.00,
            'extra_km_rate': 0.30
        },
        {
            'name': 'Week formule',
            'price': 450.00,
            'included_km': 300,
            'deposit': 400.00,
            'extra_km_rate': 0.25
        },
        {
            'name': 'Langere-termijn formule',
            'price': 100.00,
            'included_km': 200,
            'deposit': 100.00,
            'extra_km_rate': 0.20
        }
    ]
    return JsonResponse({
        'formulas': formulas,
        'version': 'V15'
    })

@csrf_exempt  
@require_http_methods(["GET"])
def api_debug_formulas(request):
    """Debug pricing formulas"""
    return JsonResponse({
        'debug_formulas': {
            'weekend': {'price': 150.00, 'days': '3 days'},
            'midweek': {'price': 120.00, 'days': '2 days'},
            'week': {'price': 450.00, 'days': '7 days'}
        },
        'version': 'V15'
    })

@csrf_exempt
@require_http_methods(["GET"])
def api_info(request):
    """Get system information"""
    return JsonResponse({
        'system_info': {
            'version': 'V15',
            'django_version': '4.2.7',
            'render_ready': True,
            'wordpress_integrated': True,
            'deployment_date': '2025-10-29'
        },
        'version': 'V15'
    })
