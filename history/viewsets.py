from rest_framework import viewsets
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer
from rest_framework.permissions import IsAuthenticated

class TransactionHistoryViewSet(viewsets.ModelViewSet):
    queryset = TransactionHistory.objects.all().order_by('-borrow_date')
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # lab techs
            return self.queryset
        return self.queryset.filter(borrower=user)  # students see only their own
