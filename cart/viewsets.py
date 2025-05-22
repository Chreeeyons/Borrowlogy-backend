# cart/viewsets.py
from rest_framework import viewsets
from .models import Cart, CartItem, Equipment
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_item(self, request, pk=None):
        print("Request data:", request.data)  # Debugging line to check incoming data
        user_id = request.data.get('user_id')  # Get the user ID from the request
        equipment_id = request.data.get('equipment_id')
        quantity = int(request.data.get('quantity', 1))
        try:
             # Get or create the cart for the user with status=False
            cart, created = Cart.objects.get_or_create(user_id=user_id, status=False)
            equipment = Equipment.objects.get(id=equipment_id)
            if equipment.quantity >= quantity:
                item, created = CartItem.objects.get_or_create(cart=cart, equipment=equipment)
                item.quantity += quantity
                item.cart = cart  # Set the cart for the item
                item.save()
                equipment.quantity -= quantity
                equipment.save()
                return Response({'status': 'Item added to cart'})
            else:
                return Response({'error': 'Not enough stock'}, status=400)
        except Equipment.DoesNotExist:
            return Response({'error': 'Material not found'}, status=404)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            material = item.material
            material.quantity_available += item.quantity
            material.save()
            item.delete()
            return Response({'status': 'Item removed from cart'})
        except CartItem.DoesNotExist:
            return Response({'error': 'CartItem not found'}, status=404)

    @action(detail=True, methods=['post'])
    def clear_cart(self, request, pk=None):
        cart = self.get_object()
        for item in cart.items.all():
            material = item.material
            material.quantity_available += item.quantity  # Restore stock
            material.save()
            item.delete()  # Remove the item from the cart
        return Response({'status': 'Cart cleared'})