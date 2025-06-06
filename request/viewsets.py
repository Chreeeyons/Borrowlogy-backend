from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Request
from .serializers import RequestSerializer

# Custom permission for lab technicians
class IsLabTechnician(permissions.BasePermission):
    """Custom permission to only allow lab technicians to approve or reject requests."""

    def has_permission(self, request, view):
        # Replace 'is_lab_technician' with the actual logic/attribute for identifying a lab technician
        return request.user.is_authenticated and request.user.is_lab_technician

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]  # Allow authenticated users for general actions

    def perform_create(self, serializer):
        """Ensure the request is linked to the authenticated user."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsLabTechnician])  # Only lab technicians can approve
    def approve(self, request, pk=None):
        """Approve a request (only lab technician should do this)."""
        request_obj = self.get_object()
        request_obj.approve()
        return Response({'status': 'Request approved'})

    @action(detail=True, methods=['post'], permission_classes=[IsLabTechnician])  # Only lab technicians can reject
    def reject(self, request, pk=None):
        """Reject a request (only lab technician should do this)."""
        request_obj = self.get_object()
        request_obj.reject()
        return Response({'status': 'Request rejected'})
