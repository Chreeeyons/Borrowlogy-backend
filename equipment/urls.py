from django.urls import path, include
from rest_framework.routers import DefaultRouter
from equipment.views import EquipmentViewSet

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),  # Include all ViewSet routes
    path('equipment/edit_equipment/', EquipmentViewSet.as_view({'put': 'edit_equipment', 'patch': 'edit_equipment'}), name='edit_equipment'),
]