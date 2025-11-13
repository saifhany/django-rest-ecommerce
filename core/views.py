from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.conf import settings
import redis
import logging

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring and load balancers.
    """
    permission_classes = []
    authentication_classes = []
    
    def get(self, request):
        """
        Check the health of the application and its dependencies.
        """
        health_status = {
            'status': 'healthy',
            'service': 'django-auth-products',
            'version': '1.0.0',
            'checks': {}
        }
        
        overall_healthy = True
        
        # Check Database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            health_status['checks']['database'] = {
                'status': 'healthy',
                'message': 'Database connection is working'
            }
        except Exception as e:
            overall_healthy = False
            health_status['checks']['database'] = {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}'
            }
            logger.error(f"Database health check failed: {str(e)}")
        
        # Check Redis/Celery Broker
        try:
            redis_url = settings.CELERY_BROKER_URL
            if redis_url and redis_url.startswith('redis://'):
                # Extract host and port from redis URL
                # Format: redis://host:port/db or redis://redis:6379/0
                parts = redis_url.replace('redis://', '').split('/')
                host_port = parts[0].split(':')
                redis_host = host_port[0] if len(host_port) > 0 else 'localhost'
                redis_port = int(host_port[1]) if len(host_port) > 1 else 6379
                r = redis.Redis(host=redis_host, port=redis_port, socket_connect_timeout=2, decode_responses=False)
                r.ping()
                health_status['checks']['redis'] = {
                    'status': 'healthy',
                    'message': 'Redis (Celery broker) is accessible'
                }
            else:
                health_status['checks']['redis'] = {
                    'status': 'unknown',
                    'message': 'Redis check not implemented for this backend'
                }
        except Exception as e:
            # Don't fail overall health check if Redis is down (optional dependency)
            health_status['checks']['redis'] = {
                'status': 'unhealthy',
                'message': f'Redis check failed: {str(e)}'
            }
            logger.warning(f"Redis health check failed: {str(e)}")
        
        # Set overall status
        if not overall_healthy:
            health_status['status'] = 'unhealthy'
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response(health_status, status=status.HTTP_200_OK)
