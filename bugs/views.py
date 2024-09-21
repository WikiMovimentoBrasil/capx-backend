from .models import Bug, Attachment
from .serializers import BugSerializer, AttachmentSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class BugViewSet(viewsets.ModelViewSet):
    serializer_class = BugSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Bug.objects.all()
        else:
            queryset = Bug.objects.filter(user=user)
        return queryset
    
    # Check if user is staff
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )       
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            return super().update(request, *args, **kwargs)
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        return response.Response("PATCH method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED) 

class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Attachment.objects.all()
        else:
            queryset = Attachment.objects.filter(bug__user=user)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        return response.Response("PATCH method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return response.Response("PUT method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )