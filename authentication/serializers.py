from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'username', 'user_type']  # add user_type if needed
        read_only_fields = ['id', 'username']  # username generated from email, so read-only
