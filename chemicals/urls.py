from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ChemicalViewSet

router = DefaultRouter()
router.register(r'chemicals', ChemicalViewSet, basename='chemical')

urlpatterns = [
    path('', include(router.urls)),
]
