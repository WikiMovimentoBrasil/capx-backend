from rest_framework import serializers
from orgs.models import Organization
from users.models import CustomUser

    
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['creation_date']