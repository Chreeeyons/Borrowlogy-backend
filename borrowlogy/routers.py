from rest_framework import routers
from authentication.viewsets import UserViewSet
from equipment.viewsets import EquipmentViewSet

router = routers.SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('equipment', EquipmentViewSet, basename='equipment')


urlpatterns = router.urls