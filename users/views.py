from .models import Profile, Territory, Language, WikimediaProject
from orgs.models import Organization
from .serializers import ProfileSerializer, TerritorySerializer, LanguageSerializer, WikimediaProjectSerializer, UsersBySkillSerializer, UsersByTagSerializer
from skills.models import Skill
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email', 'display_name', 'about']
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        queryset = Profile.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'put', 'head', 'delete', 'options']

    def get_queryset(self):
        # Only allow the logged-in user to access their own profile
        return Profile.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the requesting user is the owner of the profile
        if instance.user == request.user:

            # Verify if there are any mismatch between skill_known and skill_available
            no_value = object()

            if request.data.get('skills_known', no_value) is no_value:
                skills_known = set(map(str, instance.skills_known.all().values_list('id', flat=True)))
            else:
                skills_known = set(request.data.get('skills_known'))

            if request.data.get('skills_available', no_value) is no_value:
                skills_available = set(map(str, instance.skills_available.all().values_list('id', flat=True)))
            else:    
                skills_available = set(request.data.get('skills_available'))

            if skills_available - skills_known:
                response = {'message': 'You cannot add a skill to skills_available that is not in skills_known.'}
                return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return super().update(request, *args, **kwargs)

    # Make it possible for the user to delete their own account
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # Delete the associated CustomUser when a Profile is deleted
        user = instance.user
        instance.delete()
        user.delete()

class TerritoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializer


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


class UsersBySkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UsersBySkillSerializer

    def retrieve(self, request, *args, **kwargs):
        skill_id = self.kwargs['pk']
        skill = get_object_or_404(Skill, pk=skill_id)

        known_users = Profile.objects.filter(skills_known=skill)
        available_users = Profile.objects.filter(skills_available=skill)
        wanted_users = Profile.objects.filter(skills_wanted=skill)
        data = {
            'known': [{'id': user.id, 'display_name': user.display_name, 'username': user.user.username, 'profile_image': user.profile_image} for user in known_users],
            'available': [{'id': user.id, 'display_name': user.display_name, 'username': user.user.username, 'profile_image': user.profile_image} for user in available_users],
            'wanted': [{'id': user.id, 'display_name': user.display_name, 'username': user.user.username, 'profile_image': user.profile_image} for user in wanted_users],
        }
        return Response(data)

    def list(self, request, *args, **kwargs):
        response = {'message': 'Please provide a skill id.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Class to list users by "tags" (skills, languages, territories, wikimedia_project, affiliation) with format /tags/<tag_type>/<tag_id>/
# Example: /tags/project/1/
class UsersByTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        tag_type = self.kwargs.get('tag_type')
        tag_id = self.kwargs.get('tag_id')

        if tag_type and not tag_id.isdigit():
            response = {'message': 'Please provide a valid tag id.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if tag_type == 'skill':
            tag = get_object_or_404(Skill, pk=tag_id)
            known_users = Profile.objects.filter(skills_known=tag)
            available_users = Profile.objects.filter(skills_available=tag)
            wanted_users = Profile.objects.filter(skills_wanted=tag)
            data = {
                'known': [{'id': user.id, 'display_name': user.display_name, 'username': user.user.username, 'profile_image': user.profile_image} for user in known_users],
                'available': [{'id': user.id, 'display_name': user.display_name, 'username': user.user.username, 'profile_image': user.profile_image} for user in available_users],
                'wanted': [{'id': user.id, 'display_name': user.display_name, 'username': user.user.username, 'profile_image': user.profile_image} for user in wanted_users],
            }
    def list(self, request, *args, **kwargs):
        tag_type = kwargs.get('tag_type')
        tag_id = kwargs.get('tag_id')
        if not tag_type or not tag_id:
            return Response({'message': 'Please provide a valid tag type and tag ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if tag_type == 'skill_known':
            queryset = Profile.objects.filter(skills_known__id=tag_id)
        elif tag_type == 'skill_available':
            queryset = Profile.objects.filter(skills_available__id=tag_id)
        elif tag_type == 'skill_wanted':
            queryset = Profile.objects.filter(skills_wanted__id=tag_id)
        elif tag_type == 'language':
            queryset = Profile.objects.filter(language__id=tag_id)
        elif tag_type == 'territory':
            queryset = Profile.objects.filter(territory__id=tag_id)
        elif tag_type == 'wikimedia_project':
            queryset = Profile.objects.filter(wikimedia_project__id=tag_id)
        elif tag_type == 'affiliation':
            queryset = Profile.objects.filter(affiliation__id=tag_id)
        else:
            return Response({'message': 'Invalid tag type. Options are: skill_known, skill_available, skill_wanted, language, territory, wikimedia_project, affiliation.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(queryset, many=True).data)