from rest_framework import routers
from authentication.viewsets import UserViewSet
from cart.views import CartViewSet
from equipment.viewsets import EquipmentViewSet

router = routers.SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('equipment', EquipmentViewSet, basename='equipment')
router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = router.urls