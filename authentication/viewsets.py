from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
        users = User.objects.all().values('id', 'username', 'email')
        print(users)
        return Response({'custom_users': list(users)})
