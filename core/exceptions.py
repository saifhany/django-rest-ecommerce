from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
DEBUG = settings.DEBUG


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides standardized error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Get the view and request
    view = context.get('view')
    request = context.get('request')
    
    # Log the exception
    logger.error(
        f"Exception in {view.__class__.__name__ if view else 'Unknown'}",
        exc_info=exc,
        extra={
            'request_path': request.path if request else None,
            'request_method': request.method if request else None,
            'user': request.user.username if request and hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
        }
    )
    
    # If response is None, it means we have an unhandled exception
    if response is None:
        if DEBUG:
            # In debug mode, return detailed error
            return Response(
                {
                    'error': 'Internal Server Error',
                    'message': str(exc),
                    'detail': str(exc.__class__.__name__) if exc else None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            # In production, return generic error
            return Response(
                {
                    'error': 'Internal Server Error',
                    'message': 'An unexpected error occurred. Please try again later.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # Customize the response data
    custom_response_data = {
        'error': True,
        'status_code': response.status_code,
        'message': None,
        'details': response.data,
    }
    
    # Handle different error types
    if response.status_code == 400:
        custom_response_data['message'] = 'Bad Request'
    elif response.status_code == 401:
        custom_response_data['message'] = 'Unauthorized'
        custom_response_data['details'] = {'detail': 'Authentication credentials were not provided or are invalid.'}
    elif response.status_code == 403:
        custom_response_data['message'] = 'Forbidden'
        custom_response_data['details'] = {'detail': 'You do not have permission to perform this action.'}
    elif response.status_code == 404:
        custom_response_data['message'] = 'Not Found'
        custom_response_data['details'] = {'detail': 'The requested resource was not found.'}
    elif response.status_code == 429:
        custom_response_data['message'] = 'Too Many Requests'
        custom_response_data['details'] = {'detail': 'Rate limit exceeded. Please try again later.'}
    elif response.status_code == 500:
        custom_response_data['message'] = 'Internal Server Error'
        if not DEBUG:
            custom_response_data['details'] = {'detail': 'An unexpected error occurred.'}
    
    # Update response data
    response.data = custom_response_data
    
    return response

