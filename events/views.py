from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Events, EventParticipant, EventOrganizations
from .serializers import EventSerializer, EventParticipantSerializer, EventOrganizationsSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    # Restrict edit on event by only the organizer or staff
    def update(self, request, *args, **kwargs):
        team = EventParticipant.objects.filter(event=self.get_object(), role__in=['organizer', 'committee'])
        if request.user.pk in team.values_list('participant', flat=True) or request.user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            return Response("Only the organizer or staff can edit this event", status=status.HTTP_403_FORBIDDEN)
        
    def partial_update(self, request, *args, **kwargs):
        team = EventParticipant.objects.filter(event=self.get_object(), role__in=['organizer', 'committee'])
        if request.user.pk in team.values_list('participant', flat=True) or request.user.is_staff:
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response("Only the organizer or staff can edit this event", status=status.HTTP_403_FORBIDDEN)
        
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        # Automatically enroll the creator as an organizer
        EventParticipant.objects.create(
            event=serializer.instance, 
            participant=self.request.user, 
            role='organizer',
            confirmed_organizer=True,
            confirmed_participant=True
        )


class EventParticipantViewSet(viewsets.ModelViewSet):
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PATCH']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    # On retrieve, only the field confirmed_organizer and confirmed_participant are editable
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().retrieve(request, *args, **kwargs)
        else:
            self.serializer_class.Meta.read_only_fields += ['event', 'participant', 'role']
        
        if request.user != self.get_object().participant:
            self.serializer_class.Meta.read_only_fields += ['confirmed_participant']

        team = EventParticipant.objects.filter(event=self.get_object().event, role__in=['organizer', 'committee'])
        if request.user.pk not in team.values_list('participant', flat=True):
            self.serializer_class.Meta.read_only_fields += ['confirmed_organizer']

        return super().retrieve(request, *args, **kwargs)
        
    # Only Organizer, Commitee or Staff can create a participant
    def create(self, request, *args, **kwargs):
        team = EventParticipant.objects.filter(event=request.data['event'], role__in=['organizer', 'committee'])
        if (
            request.user.pk in team.values_list('participant', flat=True) or 
            request.user.is_staff
        ):
            # Confirmed_organizer are true and confirmed_participant are false by default
            data = request.data.copy()
            data['confirmed_organizer'] = True
            data['confirmed_participant'] = False
            request._full_data = data
            return super().create(request, *args, **kwargs)
        else:
            return Response("Only the organizer, committee or staff can create a participant", status=status.HTTP_403_FORBIDDEN)
        
    # Other users on the team cannot unconfirm a user if the user is the creator of the event
    def update(self, request, *args, **kwargs):
        team = EventParticipant.objects.filter(event=request.data['event'], role__in=['organizer', 'committee'])

        # Create a map of the fields of the request data and the self object
        # and check which fields have changed
        obj = self.get_object()
        fields = {f.name: getattr(obj, f.name) for f in obj._meta.fields}
        changed_fields = [
            field for field in request.data.keys() 
            if 
                field in fields and 
                str(request.data[field]) != str(
                    fields[field].id if hasattr(fields[field], 'id') else fields[field]
                )
        ]


        # Check if user is not staff
        if request.user.is_staff:
            return super().update(request, *args, **kwargs)

        # Check if user is not in the team
        if (request.user.pk not in team.values_list('participant', flat=True)):            
            # Check if more than one field changed and confirmed_participant is not one of them
            if request.user.pk != self.get_object().participant.pk or ( 
                len(changed_fields) > 1 and 'confirmed_participant' not in changed_fields
            ):
                return Response("Only the organizer, committee or staff can edit participants", status=status.HTTP_403_FORBIDDEN)
        
        # Check if the user is trying to unconfirm the creator of the event
        if request.data['participant'] == str(self.get_object().event.creator.pk):
            if 'confirmed_organizer' in changed_fields:
                return Response("The creator of the event cannot be unconfirmed", status=status.HTTP_403_FORBIDDEN)
            
        # Check if the user is trying to modify the confirmed_participant field and is not the participant
        if 'confirmed_participant' in changed_fields and request.user.pk != self.get_object().participant.pk:
            return Response("Only the participant can confirm or unconfirm themselves", status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)

class EventOrganizationsViewSet(viewsets.ModelViewSet):
    queryset = EventOrganizations.objects.all()
    serializer_class = EventOrganizationsSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    # On retrieve, only the field confirmed_organizer and confirmed_organization are editable
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().retrieve(request, *args, **kwargs)
        else:
            self.serializer_class.Meta.read_only_fields += ['event', 'organization', 'role']

        # Only managers of the organization can confirm the organization
        if request.user.pk not in self.get_object().organization.managers.values_list('pk', flat=True):
            self.serializer_class.Meta.read_only_fields += ['confirmed_organization']
        
        team = EventOrganizations.objects.filter(event=self.get_object().event, role__in=['organizer', 'sponsor'])
        if request.user.pk not in team.values_list('organization', flat=True):
            self.serializer_class.Meta.read_only_fields += ['confirmed_organizer']

        return super().retrieve(request, *args, **kwargs)
    
    # Only Organizer, Commitee or Staff can set a organization as envolved in the event
    def create(self, request, *args, **kwargs):
        team = EventParticipant.objects.filter(event=request.data['event'], role__in=['organizer', 'committee'])
        if (
            request.user.pk in team.values_list('participant', flat=True) or 
            request.user.is_staff
        ):
            data = request.data.copy()
            data['confirmed_organizer'] = True
            data['confirmed_organization'] = False
            request._full_data = data
            return super().create(request, *args, **kwargs)
        else:
            return Response("Only the organizer, committee or staff can create a participant", status=status.HTTP_403_FORBIDDEN)