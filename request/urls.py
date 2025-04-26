from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import RequestViewSet

router = DefaultRouter()
router.register(r'requests', RequestViewSet, basename='request')

urlpatterns = [
    path('api/', include(router.urls)),  # Include the generated viewset URLs
]
