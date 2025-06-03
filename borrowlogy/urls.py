"""
URL configuration for borrowlogy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .routers import router
from .views import health_check
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    logger.info("Health check endpoint hit")
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('', health_check),  # Health check endpoint
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include((router.urls, 'core_api'), namespace='core_api')),
        path('chemicals/', include('chemicals.urls')),
    ])),
    path('transactions/', include('transactions.urls')),
    path('auth/', include('authentication.urls')),
    path('equipment/', include('equipment.urls')),
    path('cart/', include('cart.urls')),
    path('history/', include('history.urls')),
    path('user/', include('authentication.urls')),
]