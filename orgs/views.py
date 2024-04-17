from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Organization
from .serializers import OrganizationSerializer
from users.models import CustomUser as User, Territory


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Organization.objects.all()
        else:
            return Organization.objects.filter(managers__isnull=False)
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['territory'] = [Territory.objects.get(id=id).region_name for id in data['territory']]
        data['managers'] = [User.objects.get(id=id).username for id in data['managers']]
        return Response(data)

    def get_permissions(self):
        if self.request.method in ['DELETE', 'POST']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user in instance.managers.all():
            return super().update(request, *args, **kwargs)
        
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user in instance.managers.all():
            return super().partial_update(request, *args, **kwargs)