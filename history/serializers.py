from rest_framework import serializers
from .models import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'borrower',
            'date_created',
            'borrow_date',
            'return_date',
            'status',
            'remarks'
            
        ]