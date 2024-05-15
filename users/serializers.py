from rest_framework import serializers
from .models import Profile, CustomUser
from .submodels import Territory
from orgs.models import Organization

   
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
        ]
        read_only_fields = [
            'username',
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
        ]

class TerritorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Territory
        fields = ['id', 'territory_name']

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'display_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    territory_rep = TerritorySerializer(many=True, read_only=True, source='territory')
    affiliation_rep = OrganizationSerializer(many=True, read_only=True, source='affiliation')
    
    class Meta:
        model = Profile
        fields = [
            'user',
            'profile_image',
            'display_name',
            'pronoun',
            'about',
            'wikidata_qid',
            'wiki_alt',
            'territory',
            'territory_rep',
            'language',
            'affiliation',
            'affiliation_rep',
            'wikimedia_project',
            'team',
            'skills_known',
            'skills_available',
            'skills_wanted',
            'contact',
            'social',
        ]

    # Override the update method to allow write access to the nested user object
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data is not None:
            user = instance.user
            user.email = user_data.get('email', user.email)
            user.save()
        return super().update(instance, validated_data)
   