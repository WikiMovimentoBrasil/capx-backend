from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import status, viewsets, permissions, mixins
from rest_framework.response import Response


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

