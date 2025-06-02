# cart/viewsets.py
from rest_framework import viewsets

from chemicals.models import Chemical
from .models import Cart, CartItem, Equipment
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_item(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        equipment_id = request.data.get('equipment_id')
        chemical_id = request.data.get('chemical_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            cart, created = Cart.objects.get_or_create(user=user, status=False)
            if equipment_id:
                equipment = Equipment.objects.get(id=equipment_id)
                if equipment.quantity >= quantity:
                    item, created = CartItem.objects.get_or_create(cart=cart, equipment=equipment)
                    item.quantity += quantity
                    item.save()
                    equipment.quantity -= quantity
                    equipment.save()
                    return Response({'status': 'Item added to cart'})
                else:
                    return Response({'error': 'Not enough stock'}, status=400)
            elif chemical_id:
                chemical = Chemical.objects.get(id=chemical_id)
                if chemical.mass >= quantity: #Quantity is mass for chemicals
                    item, created = CartItem.objects.get_or_create(cart=cart, chemicals=chemical)
                    item.quantity += quantity
                    item.save()
                    chemical.quantity -= quantity
                    chemical.save()
                    return Response({'status': 'Chemical added to cart'})
                else:
                    return Response({'error': 'Not enough stock'}, status=400)
        except Equipment.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)


    @action(detail=False, methods=['post'])
    def remove_items(self, request):
        cart_id = request.data.get('cart_id')
        equipment_ids = request.data.get('equipment_ids', [])


        if not cart_id or not equipment_ids:
            return Response({"error": "Missing cart_id or equipment_ids"}, status=400)

        try:
            cart = Cart.objects.get(id=cart_id)
            removed = []
            for eid in equipment_ids:
                try:
                    item = CartItem.objects.get(cart=cart, equipment_id=eid)
                    equipment = item.equipment
                    equipment.quantity += item.quantity
                    equipment.save()
                    item.delete()
                    removed.append(eid)
                except CartItem.DoesNotExist:
                    continue
            return Response({'removed_items': removed})
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)


    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        cart_id = request.data.get('cart_id')
        try:
            cart = Cart.objects.get(id=cart_id)
            for item in cart.items.all():
                equipment = item.equipment
                equipment.quantity += item.quantity
                equipment.save()
                item.delete()
            return Response({'status': 'Cart cleared'})
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)

    @action(detail=False, methods=['post'])
    def get_cart(self, request):
        user_id = request.data.get('user_id')
        print
        try:
            cart = Cart.objects.get(user_id=user_id, status=False)
            serializer = CartSerializer(cart)
            print(serializer.data)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'No active cart found'}, status=404)

        
    @action(detail=False, methods=['patch'])
    def update_item_quantity(self, request):
        cart_id = request.data.get('cart_id')
        equipment_id = request.data.get('equipment_id')
        quantity = request.data.get('quantity')
        
        try:
            quantity = int(quantity)
            cart_item = CartItem.objects.get(cart_id=cart_id, equipment_id=equipment_id)
            cart_item.quantity = quantity
            
            cart_item.save()
            return Response({
                "success": True,
                "cart_item": {
                    "cart_id": cart_id,
                    "equipment_id": equipment_id,
                    "quantity": quantity
                }
            })
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)