from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'head', 'options']

    

    


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'put', 'head', 'options']

    def get_queryset(self):
        # Only allow the logged-in user to access their own profile
        return Profile.objects.filter(user=self.request.user)

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        response = {'message': 'Delete function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the requesting user is the owner of the profile
        if instance.user == request.user:
            # Verify if there are any matches between skill_known and skill_available
            if set(list(instance.skills_known.all())) & set(list(instance.skills_available.all())):
                response = {'message': 'You cannot update the profile with matching skills.'}
                return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return super().update(request, *args, **kwargs)
        else:
            response = {'message': 'You do not have permission to update this profile.'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
