# cart/serializers.py

from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import Cart, CartItem, Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'equipment_id', 'cart_id', 'quantity', 'equipment']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the nested UserSerializer
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'items']

