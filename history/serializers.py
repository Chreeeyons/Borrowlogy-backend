from rest_framework import serializers
from .models import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    borrower_name = serializers.CharField(source='borrower.get_full_name', read_only=True)

    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'borrower',
            'borrower_name',
            'equipment',
            'equipment_name',
            'quantity',
            'borrow_date',
            'return_date',
            'status',
            'remarks'
        ]
