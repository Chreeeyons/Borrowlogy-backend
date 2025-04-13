# cart/viewsets.py
from rest_framework import viewsets
from .models import Cart, CartItem, Material
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        material_id = request.data.get('material_id')
        quantity = int(request.data.get('quantity', 1))
        remarks = request.data.get('remarks', '')  # Capture remarks
        try:
            material = Material.objects.get(id=material_id)
            if material.quantity_available >= quantity:
                item, created = CartItem.objects.get_or_create(cart=cart, material=material)
                item.quantity += quantity
                item.remarks = remarks  # Set remarks
                item.save()
                material.quantity_available -= quantity
                material.save()
                return Response({'status': 'Item added to cart'})
            else:
                return Response({'error': 'Not enough stock'}, status=400)
        except Material.DoesNotExist:
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
