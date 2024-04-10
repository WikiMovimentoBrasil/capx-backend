from rest_framework import serializers
from .models import Profile, CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'is_staff',
            'is_active',
            'date_joined',
        ]

    def get_fields(self):
        fields = super().get_fields()
        fields["username"].read_only = True
        return fields


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'pronoun',
            'profile_image',
            'display_name',
            'birthday',
            'about',
            'twitter',
            'facebook',
            'instagram',
            'telegram',
            'github',
            'irc',
            'wiki_alt',
            'wiki_develop',
            'contact_method',
            'region',
            'language',
            'affiliation',
            'wikimedia_project',
            'area_of_interest',
            'skills_known',
            'skills_wanted',
        ]

    def to_representation(self, instance):
        profile_data = super(ProfileSerializer, self).to_representation(instance)
        user_data = UserSerializer(instance.user).data
        return {**user_data, **profile_data}

    