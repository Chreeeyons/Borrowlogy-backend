from django.urls import include, path
from rest_framework.routers import DefaultRouter

from history.views import HistoryViewSet

router = DefaultRouter()
router.register(r'history', HistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),  # Include all ViewSet routes
]