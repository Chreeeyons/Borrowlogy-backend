from rest_framework import serializers
from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'user', 'equipment', 'quantity', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'quantity', 'equipment']

    def update(self, instance, validated_data):
        """Allow only status updates (approve/reject) by lab technician."""
        status = validated_data.get('status', instance.status)
        
        # Ensure that the status is one of the allowed values
        if status not in dict(Request.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid status. Must be 'approved' or 'rejected'.")

        instance.status = status
        instance.save()
        return instance
