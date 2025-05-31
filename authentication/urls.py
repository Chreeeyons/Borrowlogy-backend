from django.urls import include, path
from authentication.viewsets import UserViewSet
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # Include all ViewSet routes
]
