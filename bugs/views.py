from .models import Bug, Attachment
from .serializers import BugSerializer, BugStaffSerializer, AttachmentSerializer
from rest_framework import viewsets, permissions


class BugViewSet(viewsets.ModelViewSet):
    serializer_class = BugSerializer
    queryset = Bug.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return BugStaffSerializer
        else:
            return BugSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
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
