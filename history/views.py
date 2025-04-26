from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from .models import TransactionHistory as History
from .serializers import TransactionHistorySerializer as HistorySerializer
from rest_framework.decorators import action
from cart.serializers import CartSerializer  # Import the CartSerializer


class HistoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, retrieving, and creating history records.
    """
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_queryset(self):
        # Restrict the queryset to the authenticated user's history records
        # return self.queryset.filter(user=self.request.user).order_by('-timestamp')
        pass

    @action(detail=False, methods=['post'])
    def create_history(self, request):
        """
        Custom action to create a new history record.
        """
        data = request.data.copy()
        user_id = request.data["user_id"]
        cart_id = request.data["cart_id"]
        borrower_date = request.data["borrower_date"]
        remarks = request.data["remarks"]
        print(user_id, cart_id, borrower_date, remarks)

        # Create a new history record
        history = History.objects.create(
            borrower_id=user_id,
            status='Pending',
            borrow_date=borrower_date,
            remarks=remarks
        )
        history.save()
        
        cart = Cart.objects.get(id=cart_id)
        cart.TransactionHistory= history
        cart.status = True
        cart.save()

        return Response({'status': 'History record created successfully', 'history_id': history.id})
    
    @action(detail=False, methods=['post'])
    def get_all_history_borrower(self, request):
        """
        Custom action to retrieve all history records for the authenticated user.
        """
        user_id = request.data.get('user_id')
        if user_id :
            history_records = self.queryset.filter(borrower_id=user_id).order_by('-borrow_date')
            serializer = self.get_serializer(history_records, many=True)

            # Add the serialized cart data to each history record
            history_data = serializer.data
            for index, record in enumerate(history_records):
                cart = Cart.objects.get(TransactionHistory=record.id)
                cart_serializer = CartSerializer(cart)  # Serialize the Cart object
                history_data[index]["cart"] = cart_serializer.data  # Add serialized cart data
            return Response(serializer.data)
        
        else:
            history_records = self.queryset.filter(status='Pending').order_by('-borrow_date')
            serializer = self.get_serializer(history_records, many=True)

            # Add the serialized cart data to each history record
            history_data = serializer.data
            for index, record in enumerate(history_records):
                cart = Cart.objects.get(TransactionHistory=record.id)
                cart_serializer = CartSerializer(cart)  # Serialize the Cart object
                history_data[index]["cart"] = cart_serializer.data  # Add serialized cart data
            return Response(serializer.data)