# from rest_framework import serializers
# from .models import Request

# class RequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Request
#         fields = ['id', 'user', 'equipment', 'quantity', 'status', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at']

#     def update(self, instance, validated_data):
#         """Allow only status updates (approve/reject) by lab technician."""
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()
#         return instance
