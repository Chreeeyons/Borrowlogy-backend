from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Chemical
from .serializers import ChemicalSerializer

class ChemicalViewSet(viewsets.ModelViewSet):
    queryset = Chemical.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ChemicalSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    # GET endpoint with optional filtering
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_chemicals(self, request):
        is_hazardous = request.query_params.get('is_hazardous', None)
        qs = Chemical.objects.all()
        if is_hazardous is not None:
            if is_hazardous.lower() == 'true':
                qs = qs.filter(is_hazardous=True)
            elif is_hazardous.lower() == 'false':
                qs = qs.filter(is_hazardous=False)

        chemicals = qs.values(
            'id', 'chemical_name', 'mass', 'brand_name',
            'is_hazardous', 'location', 'expiration_date'
        )
        return Response({'chemicals': list(chemicals)})

    # POST endpoint to add or update chemical (upsert)
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def add_chemical(self, request):
        data = request.data
        
        chemical_name = data.get('chemical_name')
        mass = data.get('mass')
        brand_name = data.get('brand_name')
        
        if not all([chemical_name, mass, brand_name]):
            return Response({'error': 'Missing required identifying fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        chemical = Chemical.objects.filter(
            chemical_name=chemical_name,
            mass=mass,
            brand_name=brand_name
        ).first()

        if chemical:
            serializer = ChemicalSerializer(chemical, data=data, partial=True)
            action_str = 'updated'
        else:
            serializer = ChemicalSerializer(data=data)
            action_str = 'added'

        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Chemical {action_str} successfully', 'chemical': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT/PATCH endpoint to edit chemical
    @action(detail=False, methods=['put', 'patch'], permission_classes=[AllowAny])
    def edit_chemical(self, request):
        pk = request.data.get('pk')
        if not pk:
            return Response({'error': "Missing 'pk' in request body"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            chemical = Chemical.objects.get(pk=pk)
        except Chemical.DoesNotExist:
            return Response({'error': 'Chemical not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChemicalSerializer(chemical, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Chemical updated successfully', 'chemical': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE endpoint to delete chemical
    @action(detail=False, methods=['delete'], permission_classes=[AllowAny])
    def delete_chemical(self, request):
        pk = request.data.get('pk')
        if not pk:
            return Response({'error': "Missing 'pk' in request body"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            chemical = Chemical.objects.get(pk=pk)
            chemical.delete()
            return Response({'message': 'Chemical deleted successfully'})
        except Chemical.DoesNotExist:
            return Response({'error': 'Chemical not found'}, status=status.HTTP_404_NOT_FOUND)
