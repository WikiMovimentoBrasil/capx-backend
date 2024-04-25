from rest_framework import serializers
from .models import Events, EventParticipant, EventOrganizations

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'
        read_only_fields = ['creator', 'created_at']
        
class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class EventOrganizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizations
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
