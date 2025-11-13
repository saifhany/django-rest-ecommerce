from django.contrib import admin
from django.urls import path, include
from .views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health Check
    path('health', HealthCheckView.as_view(), name='health-check'),
    
    # API Routes
    path('api/auth/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
]
