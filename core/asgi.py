# Asynchronous Server Gateway Interface 
# serve async & websocket
import os
from django.core.asgi import get_asgi_application
# let our framework know our settings located in core/settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_asgi_application()
