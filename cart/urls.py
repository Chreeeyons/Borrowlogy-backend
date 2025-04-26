# cart/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    # path('get_cart/<int:user_id>', CartViewSet.as_view({'get': 'get_cart'}), name='get_cart'),
    path('', include(router.urls)),  # Include all ViewSet routes
    #path('cart/add_item', CartViewSet.as_view({'post': 'add_item'}), name='add_item'),
]
