# cart/serializers.py

from rest_framework import serializers

from authentication.serializers import UserSerializer
from chemicals.models import Chemical
from .models import Cart, CartItem, Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class ChemicalSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display', read_only=True)

    class Meta:
        model = Chemical
        fields = [
            'id', 'chemical_name', 'mass', 'brand_name',
            'hazard_type', 'hazard_type_display', 'location', 'expiration_date'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()
    chemicals = ChemicalSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'equipment_id', 'cart_id', 'quantity', 'equipment', 'chemicals']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use the nested UserSerializer
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'items']


