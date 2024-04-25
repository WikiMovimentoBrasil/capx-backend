from rest_framework import serializers
from .models import Profile, CustomUser

   
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'middle_name',
            'last_name',
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

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'pronoun',
            'profile_image',
            'display_name',
            'birthday',
            'about',
            'irc',
            'wiki_alt',
            'wiki_develop',
            'email',
            'contact_method',
            'territory',
            'language',
            'affiliation',
            'wikimedia_project',
            'skills_known',
            'skills_available',
            'skills_wanted',
        ]

    # Override the update method to allow write access to the nested user object
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data is not None:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.middle_name = user_data.get('middle_name', user.middle_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()
        return super().update(instance, validated_data)
   