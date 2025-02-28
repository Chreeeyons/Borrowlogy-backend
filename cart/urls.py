from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('equipment/', include('equipment.urls')),  # Existing app
    path('cart/', include('cart.urls')),  # New app
]