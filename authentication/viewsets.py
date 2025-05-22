from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from .models import TransactionHistory as History

from history.models import TransactionHistory
from history.serializers import TransactionHistorySerializer
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    

    # Custom GET method using @action decorator
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def userget(self, request):
        """
        Custom GET endpoint to list user data without affecting the default behavior.
        Accessible at /users/custom/
        """
        users = User.objects.all().values('id', 'name', 'email' )

        for user in users:
        
            item = TransactionHistory.objects.filter(borrower_id=user['id'])

            # Add the serialized cart data to each history record
            history_data = item.values('id', 'status', 'borrow_date', 'return_date')

            user['transactions'] = history_data

        return Response({'custom_users': list(users)})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def create_borrower(self, request):
        """
        Custom POST endpoint to create a user with the 'borrower' user type.
        Accessible at /users/create_borrower/
        """
        data = request.data.copy()
        data['user_type'] = 'borrower'  # Set the user type to 'borrower'

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'User saved successfully'})
        return Response({'error': 'Failed to save user'}, status=400)
    
