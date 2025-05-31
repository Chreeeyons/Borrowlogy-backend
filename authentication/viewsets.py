# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# # from .models import TransactionHistory as History

# from history.models import TransactionHistory
# from history.serializers import TransactionHistorySerializer
# from .models import User
# from .serializers import UserSerializer
# from rest_framework.permissions import AllowAny


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]


#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def create_borrower(self, request):
#         """
#         Custom POST endpoint to create a user with the 'borrower' user type.
#         Accessible at /users/create_borrower/
#         """
#         data = request.data.copy()
#         data['user_type'] = 'borrower'  # Set the user type to 'borrower'

#         serializer = self.get_serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': 'User saved successfully'})
#         return Response({'error': 'Failed to save user'}, status=400)
    
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from history.models import TransactionHistory
from history.serializers import TransactionHistorySerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def list_users_with_transactions(self, request):
        users = User.objects.all()
        results = []
        for user in users:
            transactions = TransactionHistory.objects.filter(borrower_id=user.id)
            transactions_serialized = TransactionHistorySerializer(transactions, many=True).data
            user_data = UserSerializer(user).data
            user_data['transactions'] = transactions_serialized
            results.append(user_data)

        return Response({'users': results}, status=status.HTTP_200_OK)
    
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
        data = request.data.copy()
        data['user_type'] = 'borrower'

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'User created successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def by_email(self, request):
            try:
                email = request.data.get('email')
                if not email:
                    return Response({'error': 'Email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
                user = self.get_queryset().get(email=email)
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
