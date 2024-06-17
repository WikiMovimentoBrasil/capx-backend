from .models import Profile, Territory, Language, WikimediaProject
from .serializers import ProfileSerializer, TerritorySerializer, LanguageSerializer, WikimediaProjectSerializer, UsersBySkillSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response


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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the requesting user is the owner of the profile
        if instance.user == request.user:
            # Verify if there are any matches between skill_known and skill_available
            if set(request.data.get('skills_known', [])) & set(request.data.get('skills_available', [])):
                response = {'message': 'You cannot update the profile with matching skills.'}
                return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return super().update(request, *args, **kwargs)


class ListTerritoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {territory.id: str(territory) for territory in queryset}
        return Response(data)


class ListLanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {language.id: str(language) for language in queryset}
        return Response(data)


class ListWikimediaProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WikimediaProject.objects.all()
    serializer_class = WikimediaProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {project.id: str(project) for project in queryset}
        return Response(data)


# List users that set an queried skill as known, available or wanted. Output as three lists.
class UsersBySkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UsersBySkillSerializer

    def retrieve(self, request, *args, **kwargs):
        skill_id = self.kwargs['pk']
        known_users = Profile.objects.filter(skills_known=skill_id)
        available_users = Profile.objects.filter(skills_available=skill_id)
        wanted_users = Profile.objects.filter(skills_wanted=skill_id)
        data = {
            'known': [user.id for user in known_users],
            'available': [user.id for user in available_users],
            'wanted': [user.id for user in wanted_users],
        }
        return Response(data)

    def list(self, request, *args, **kwargs):
        response = {'message': 'Please provide a skill id.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
   
