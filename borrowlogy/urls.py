from django.contrib import admin
from django.urls import path, include
from authentication.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('equipment/', include('equipment.urls')),
    path('transactions/', include('transactions.urls')),
    path('auth/', include('authentication.urls')),
    path("", homepage, name="homepage"),
    path('menu/', include('menu.urls')),
    path('menu/', include('menu.urls')),
    path('equipment/', include('equipment.urls')),
    path("api/menu/", include("menu.urls")),
]
