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

from cart.models import Cart, CartItem
from .models import User
from .serializers import UserSerializer
from history.models import TransactionHistory
from history.serializers import TransactionHistorySerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
import datetime
import requests


GOOGLE_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

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
            history_data = item.values('id', 'status', 'borrow_date', 'return_date', 'labtech_remarks', 'remarks', 'cart')
            for history in history_data:
                print(history["cart"])
                cart, created = Cart.objects.filter(id=history['cart']).first(), False
                # Get all CartItems for the cart
                cart_items = CartItem.objects.filter(cart=cart)#.values('id', 'return_quantity', 'return_date', 'approved')

                # Group and sum quantities manually
                grouped_items = {}
                for item in cart_items:
                    equipment_id = "equip_"+str(item.equipment.id) if item.equipment else "chem_"+str(item.chemicals.id)
                    equipment_name = item.equipment.name if item.equipment else item.chemicals.chemical_name 
                    if equipment_id not in grouped_items:   
                        grouped_items[equipment_id] = {
                            'equipment_id': equipment_id,
                            'equipment_name': equipment_name,
                            'return_quantity': item.return_quantity,
                            'return_date': item.return_date,
                            'total_quantity': 0
                        }
                    grouped_items[equipment_id]['total_quantity'] += item.quantity

                # Convert grouped_items to a list
                grouped_items_list = list(grouped_items.values())
                history['cart_items'] = grouped_items_list

                # history['cart_items'] = Cart_Items.objects.filter(id=history['cart']).values('id', 'status', 'items')
                # history['cart_items'] = list(history['cart_items'])
                # Get the cart items for each history record
                #if history['cart']:
                    #history['cart']['items'] = Cart.objects.filter(id=history['cart_id']).values('id', 'status', 'items')
             #cart = Cart.objects.filter(cart_id=history_data['id']).values('id', 'status')

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
    
    # @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    # def by_email(self, request):
    #         try:
    #             email = request.data.get('email')
    #             if not email:
    #                 return Response({'error': 'Email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    #             user = self.get_queryset().get(email=email)
    #             serializer = self.get_serializer(user)
    #             if serializer:
    #                 user = User.objects.get(email=email)
    #                 user.last_login = datetime.datetime.now()
    #                 user.save()
                        
    #             return Response(serializer.data)
    #         except User.DoesNotExist:
    #             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['patch'], permission_classes=[AllowAny])
    def update_history(self, request, pk=None):
        items = request.data.get('items', [])
        transaction_id = request.data.get('transaction_id')
        cart_id = request.data.get('cart_id')
        remarks = request.data.get('remarks', '')
  
        if not items:
            return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction = TransactionHistory.objects.get(id=transaction_id)

        for item in items:
            print(item['equipment_id'])
            item_type = item['equipment_id'].split('_')[0]  # Determine if it's equipment or chemical
            item_id = item['equipment_id'].split('_')[-1]  # Extract the ID from the equipment_id
            print(cart_id, )
            if item_type == 'equip':
                    cart_item = CartItem.objects.get(cart_id=cart_id, equipment=item_id)
                    equipment = cart_item.equipment
                    equipment.quantity += cart_item.quantity #item['return_quantity']
                    cart_item.return_quantity =  cart_item.quantity #item['return_quantity']
                    cart_item.return_date = datetime.date.today()  # Set return date to today
                    equipment.save()
                    cart_item.save()
                    transaction.remarks = remarks
                    transaction.status = 'Returned'
                    transaction.save()

            elif item_type == 'chem':
                    cart_item = CartItem.objects.get(cart=cart_id, chemicals_id=item_id)
                    chemicals = cart_item.chemicals
                    chemicals.mass +=  cart_item.quantity  #['return_quantity']
                    cart_item.return_quantity = cart_item.quantity #item['return_quantity']
                    cart_item.return_date = datetime.date.today()  # Set return date to today
                    chemicals.save()
                    cart_item.save()
                    transaction.remarks = remarks
                    transaction.status = 'Returned'
                    transaction.save()

        return Response({'message': 'Returned successfully'}, status=status.HTTP_200_OK)
    
              


    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        print("HERE")
        access_token = request.data.get('access_token')
        print(access_token)

        if not access_token:
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            google_response = requests.get(GOOGLE_URL, headers={'Authorization': f'Bearer {access_token}'})
        except requests.RequestException:
            return Response({'error': 'Failed to connect to Google'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if google_response.status_code != 200:
            return Response({'error': 'Failed to authenticate with Google'}, status=status.HTTP_400_BAD_REQUEST)

        google_data = google_response.json()
        email = google_data.get('email')
        first_name = google_data.get('given_name')
        last_name = google_data.get('family_name')
        google_id = google_data.get('sub')

        if not email:
            return Response({'error': 'Email not found in Google response'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # Update missing fields if necessary
            if not user.first_name:
                user.first_name = first_name
            if not user.last_name:
                user.last_name = last_name
            if hasattr(user, 'google_id') and not user.google_id:
                user.google_id = google_id
            user.save()
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Log the user in (without password if you're relying solely on Google)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        print(request.user.is_authenticated)
        return Response({'message': 'Login successful', 'user_type': request.user.user_type, 'user_id': request.user.id}, status=status.HTTP_200_OK)
        return Response

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def logout(self, request):
        """
        Logs out the current user (session auth).
        Accessible at /users/logout/
        """
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
