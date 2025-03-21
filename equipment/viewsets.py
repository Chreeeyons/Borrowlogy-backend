from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Equipment
from .serializers import EquipmentSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    permission_classes = [AllowAny]

    # Custom GET method using @action decorator
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_equipment(self, request):
        """
        Custom GET endpoint to list user data without affecting the default behavior.
        Accessible at /users/custom/
        """
        equipment = Equipment.objects.all().values('id','name', 'quantity')
        print(equipment)
        return Response({'equipment': list(equipment)})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def add_equipment(self, request):
        """
        Custom endpoint to add new equipment.
        Accessible at /equipment/add_equipment/
        """
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Equipment added successfully', 'equipment': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[AllowAny])
    def edit_equipment(self, request):
        """
        Custom endpoint to edit existing equipment.
        Accessible at /equipment/edit_equipment/
        Expects 'pk' in request body.
        """
        pk = request.data.get("pk")  # Extract primary key from request body

        if not pk:
            return Response({"error": "Missing 'pk' in request body"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response({'error': 'Equipment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EquipmentSerializer(equipment, data=request.data, partial=True)  # Use partial=True for PATCH
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Equipment updated successfully', 'equipment': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], permission_classes=[AllowAny])
    def delete_equipment(self, request):
        """
        Custom endpoint to delete equipment.
        Accessible at /equipment/delete_equipment/
        Expects 'pk' in request body.
        """
        pk = request.data.get("pk")

        if not pk:
            return Response({"error": "Missing 'pk' in request body"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            equipment = Equipment.objects.get(pk=pk)
            equipment.delete()
            return Response({'message': 'Equipment deleted successfully'}, status=status.HTTP_200_OK)
        except Equipment.DoesNotExist:
            return Response({'error': 'Equipment not found'}, status=status.HTTP_404_NOT_FOUND)