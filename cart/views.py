from rest_framework import viewsets
from equipment.models import Equipment
from history.models import TransactionHistory
from .models import Cart, CartItem, Material
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_item(self, request, pk=None):
        user_id = request.data.get('user_id')  # Get the user ID from the request
        equipment_id = request.data.get('equipment_id')
        quantity = int(request.data.get('quantity'))
        try:
             # Get or create the cart for the user with status=False
            cart, created = Cart.objects.get_or_create(user_id=user_id, status=False)
            equipment = Equipment.objects.get(id=equipment_id)
            if equipment.quantity >= quantity:
                cart_items = CartItem.objects.filter(cart=cart, equipment=equipment)

                if cart_items.exists():
                    # If duplicates exist, sum their quantities and consolidate them
                    total_quantity = sum(item.quantity for item in cart_items)
                    cart_item = cart_items.first()  # Use the first item
                    cart_item.quantity = total_quantity + quantity  # Update the quantity
                    cart_item.save()

                    # Delete the duplicate items (except the first one)
                    cart_items.exclude(id=cart_item.id).delete()
                else:
                    # If no duplicates exist, create a new CartItem
                    cart_item = CartItem.objects.create(cart=cart, equipment=equipment, quantity=quantity)
                equipment.quantity -= quantity
                equipment.save()
            
                return Response({'status': 'Item added to cart'})
            else:
                return Response({'error': 'Not enough stock'}, status=400)
        except Equipment.DoesNotExist:
            return Response({'error': 'Material not found'}, status=404)

    # @action(detail=True, methods=['delete'])
    # def remove_item(self, request, pk=None):
    #     cart_id = request.data.get('cart_id')
    #     try:
    #         cart = CartItem.objects.delete(id=cart_id)
    #         return Response({'status': 'cart cleared successfully'})
    #     except CartItem.DoesNotExist:
    #         return Response({'error': 'CartItem not found'}, status=404)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request, pk=None):
        cart_id = request.data.get('cart_id')
        try:
                # Retrieve the cart
            cart = Cart.objects.get(id=cart_id)

            # Retrieve all CartItems associated with the cart
            cart_items = CartItem.objects.filter(cart=cart)

            # Iterate through each CartItem
            for item in cart_items:
                # Add the CartItem quantity back to the Equipment quantity
                equipment = item.equipment
                equipment.quantity += item.quantity
                equipment.save()

            # Delete all CartItems associated with the cart
            cart_items.delete()

            return Response({'status': 'cart cleared successfully'}, status=200)
        except CartItem.DoesNotExist:
            return Response({'error': 'CartItem not found'}, status=404)
    
    @action(detail=False, methods=['post'])
    def get_cart (self, request, pk=None):
        try:
            # Get or create the cart for the user with status=False
            cart, created = Cart.objects.get_or_create(user_id=request.data.get('user_id'), status=False)

            # Get all CartItems for the cart
            cart_items = CartItem.objects.filter(cart=cart)

            # Group and sum quantities manually
            grouped_items = {}
            for item in cart_items:
                equipment_id = item.equipment.id
                equipment_name = item.equipment.name
                if equipment_id not in grouped_items:
                    grouped_items[equipment_id] = {
                        'equipment_id': equipment_id,
                        'equipment_name': equipment_name,
                        'total_quantity': 0
                    }
                grouped_items[equipment_id]['total_quantity'] += item.quantity

            # Convert grouped_items to a list
            grouped_items_list = list(grouped_items.values())

            return Response({
                'cart_id': cart.id,
                'user_id': cart.user_id,
                'items': grouped_items_list
            })
        except Equipment.DoesNotExist:
            return Response({'error': 'Material not found'}, status=404)

    @action(detail=False, methods=['patch'])
    def approve_cart(self, request, pk=None):
        cart_items = request.data.get('cart_items')
        history_id = request.data.get('history_id')
        try:
            for item in cart_items:
                # Update the approved status of each CartItem
                cart_item = CartItem.objects.get(id=item['id'])
                cart_item.approved = True
                cart_item.save()
            transactionhistory = TransactionHistory.objects.filter(id=history_id)
            transactionhistory.update(status='Borrowed')
            return Response({'status': 'cart approved successfully'}, status=200)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)