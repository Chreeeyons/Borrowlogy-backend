from django.urls import include, path
from authentication.viewsets import UserViewSet
from . import views
from .views import homepage
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    # path('get_cart/<int:user_id>', CartViewSet.as_view({'get': 'get_cart'}), name='get_cart'),
    path('', include(router.urls)),  # Include all ViewSet routes
    #path('cart/add_item', CartViewSet.as_view({'post': 'add_item'}), name='add_item'),
]
