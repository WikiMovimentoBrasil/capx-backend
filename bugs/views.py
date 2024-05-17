from .models import Bug, Attachment
from .serializers import BugSerializer, AttachmentSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class BugViewSet(viewsets.ModelViewSet):
    serializer_class = BugSerializer
    queryset = Bug.objects.all()

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

        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Attachment.objects.all()
        else:
            queryset = Attachment.objects.filter(bug__user=user)
        return queryset
