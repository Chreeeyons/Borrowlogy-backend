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
from authentication.views import homepage
from .routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transactions/', include('transactions.urls')),
    path('auth/', include('authentication.urls')),
    path("", homepage, name="homepage"),
    path('equipment/', include('equipment.urls')),
    path('api/', include((router.urls, 'core_api'), namespace = 'core_api')),
    path('cart/', include('cart.urls')),  # Include the cart app's URLs
    path('history/', include('history.urls')),  # Include the history app's URLs
    path('user/', include('authentication.urls')),  # Include the history app's URLs

]