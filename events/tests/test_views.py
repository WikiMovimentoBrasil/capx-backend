from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from rest_framework import status
from rest_framework.test import APIClient
from events.models import Events, EventParticipant, EventOrganizations
from events.serializers import EventParticipantSerializer
from users.models import CustomUser
import secrets
import datetime


class EventViewSetTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_event_list(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_create(self):
        event_data = {
            'name': 'New Event',
            'type_of_location': 'hybrid',
            'time_begin': '2021-10-10 10:00:00+00:00',
            'time_end': '2021-10-10 12:00:00+00:00',
        }

        response = self.client.post('/events/', event_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Event')
        self.assertEqual(response.data['type_of_location'], 'hybrid')
        self.assertEqual(response.data['time_begin'], '2021-10-10T10:00:00Z')
        self.assertEqual(response.data['time_end'], '2021-10-10T12:00:00Z')
        self.assertEqual(response.data['creator'], self.user.id)
        self.assertEqual(response.data['team'][0], self.user.id)

        response = self.client.get('/events_participants/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event'], 1)
        self.assertEqual(response.data['participant'], self.user.id)
        self.assertEqual(response.data['role'], 'organizer')
        self.assertEqual(response.data['confirmed_organizer'], True)
        self.assertEqual(response.data['confirmed_participant'], True)

    def test_event_detail(self):
        event = Events.objects.create(
            name='Sample Event',
            type_of_location='virtual',
            time_begin='2021-10-10 10:00:00+00:00',
            time_end='2021-10-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )

        response = self.client.get(f'/events/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Event')
        self.assertEqual(response.data['type_of_location'], 'virtual')
        self.assertEqual(response.data['time_begin'], '2021-10-10T10:00:00Z')
        self.assertEqual(response.data['time_end'], '2021-10-10T12:00:00Z')
        self.assertEqual(response.data['creator'], self.user.id)

    def test_event_update(self):
        event = Events.objects.create(
            name='Sample Event',
            type_of_location='virtual',
            time_begin='2021-10-10 10:00:00+00:00',
            time_end='2021-10-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )

        event_data = {
            'name': 'New Event',
            'type_of_location': 'hybrid',
            'time_begin': '2021-10-10 10:00:00+00:00',
            'time_end': '2021-10-10 12:00:00+00:00',
        }

        response = self.client.put(f'/events/{event.id}/', event_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        EventParticipant.objects.create(
            event=event, 
            participant=self.user, 
            role='volunteer'
        )
        response = self.client.put(f'/events/{event.id}/', event_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        EventParticipant.objects.create(
            event=event, 
            participant=self.user, 
            role='organizer'
        )
        response = self.client.put(f'/events/{event.id}/', event_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_partial_update(self):
        event = Events.objects.create(
            name='Sample Event',
            type_of_location='virtual',
            time_begin='2021-10-10 10:00:00+00:00',
            time_end='2021-10-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )

        event_data = {
            'name': 'New Event',
        }

        response = self.client.patch(f'/events/{event.id}/', event_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        EventParticipant.objects.create(
            event=event, 
            participant=self.user, 
            role='volunteer'
        )
        response = self.client.patch(f'/events/{event.id}/', event_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        EventParticipant.objects.create(
            event=event, 
            participant=self.user, 
            role='organizer'
        )
        response = self.client.patch(f'/events/{event.id}/', event_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_delete(self):
        event = Events.objects.create(
            name='Sample Event',
            type_of_location='virtual',
            time_begin='2021-10-10 10:00:00+00:00',
            time_end='2021-10-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )
        EventParticipant.objects.create(
            event=event, 
            participant=self.user, 
            role='organizer'
        )

        response = self.client.delete(f'/events/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Set user as staff
        self.user.is_staff = True
        self.user.save()
        response = self.client.delete(f'/events/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_fields(self):
        event_data = {
            'name': 'New Event',
            'type_of_location': 'hybrid',
            'time_begin': '2021-10-10 10:00:00+00:00',
            'time_end': '2021-10-10 12:00:00+00:00',
        }

        create = self.client.post('/events/', event_data)
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)

        # Update event with invalid openstreetmap_id
        event_data = {
            'openstreetmap_id': 'https://www.openstreetmap.org/nothing/12345',
        }
        response = self.client.patch(f'/events/1/', event_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Update event with invalid wikidata_qid
        event_data = {
            'wikidata_qid': 'L12345',
        }
        response = self.client.patch(f'/events/1/', event_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Update event with invalid location type
        event_data = {
            'type_of_location': 'invalid',
        }  
        response = self.client.patch(f'/events/1/', event_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EventParticipantCreateTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test3', password=str(secrets.randbits(16)))
        self.other_user = CustomUser.objects.create_user(username='test4', password=str(secrets.randbits(16)))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_event_participant_create(self):        
        event = Events.objects.create(
            name='Event Sample',
            type_of_location='hybrid',
            time_begin='2021-11-10 10:00:00+00:00',
            time_end='2021-11-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )

        EventParticipant.objects.create(
            event=event,
            participant=self.user,
            role='organizer'
        )

        event_participant_data = {
            'event': event.id,
            'participant': self.other_user.id,
            'role': 'volunteer',
        }

        response = self.client.post('/events_participants/', event_participant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['event'], event.id)
        self.assertEqual(response.data['participant'], self.other_user.id)
        self.assertEqual(response.data['role'], 'volunteer')
        self.assertEqual(response.data['confirmed_organizer'], True)
        self.assertEqual(response.data['confirmed_participant'], False)

class EventParticipantTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password=str(secrets.randbits(16)))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_event_participant_list(self):
        response = self.client.get('/events_participants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_participant_detail(self):
        event = Events.objects.create(
            name='Sample Event',
            type_of_location='virtual',
            time_begin='2021-10-10 10:00:00+00:00',
            time_end='2021-10-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )

        event_participant = EventParticipant.objects.create(
            event=event,
            participant=self.user,
            role='organizer',
            confirmed_organizer=True,
            confirmed_participant=True,
        )

        response = self.client.get(f'/events_participants/{event_participant.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event'], event.id)
        self.assertEqual(response.data['participant'], self.user.id)
        self.assertEqual(response.data['role'], 'organizer')
        self.assertEqual(response.data['confirmed_organizer'], True)
        self.assertEqual(response.data['confirmed_participant'], True)

    def test_event_participant_update(self):
        
        # Create an event and add the user as an organizer
        event = Events.objects.create(
            name='Sample Event',
            type_of_location='virtual',
            time_begin='2021-10-10 10:00:00+00:00',
            time_end='2021-10-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )
        organizer_participant = EventParticipant.objects.create(
            event=event,
            participant=self.user,
            role='organizer',
            confirmed_organizer=True,
            confirmed_participant=True,
        )

        # Create a new user
        new_user = CustomUser.objects.create_user(
            username='test2', 
            password=str(secrets.randbits(16))
        )

        # Create an event participant
        new_user_participant = EventParticipant.objects.create(
            event=event,
            participant=new_user,
            role='volunteer',
            confirmed_organizer=True,
            confirmed_participant=False,
        )

        # Try to confirm the new user as a participant
        event_participant_data = {
            'id': new_user_participant.id,
            'event': event.id,
            'participant': new_user.id,
            'role': 'volunteer',
            'confirmed_organizer': True,
            'confirmed_participant': True,
        }
        response = self.client.put(f'/events_participants/{new_user_participant.id}/', event_participant_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Only the participant can confirm or unconfirm themselves')

        # Force new_user authentication
        self.client.force_authenticate(new_user)

        # Try to confirm the new user as a participant
        event_participant_data = {
            'id': new_user_participant.id,
            'event': event.id,
            'participant': new_user.id,
            'role': 'volunteer',
            'confirmed_organizer': True,
            'confirmed_participant': True,
        }
        response = self.client.put(f'/events_participants/{new_user_participant.id}/', event_participant_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to unconfirm the creator of the event
        event_participant_data = {
            'id': organizer_participant.id,
            'event': event.id,
            'participant': self.user.id,
            'role': 'organizer',
            'confirmed_organizer': False,
            'confirmed_participant': True,
        }
        response = self.client.put(f'/events_participants/{organizer_participant.id}/', event_participant_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'The creator of the event cannot be unconfirmed')

        # Try to unconfirm the creator of the event as a staff
        new_user.is_staff = True
        new_user.save()
        response = self.client.put(f'/events_participants/{organizer_participant.id}/', event_participant_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_participant_delete(self):
        event = Events.objects.create(
            name='Sample Event',
            type_of_location='virtual',
            time_begin='2021-10-10 10:00:00+00:00',
            time_end='2021-10-10 12:00:00+00:00',
            creator=CustomUser.objects.get(id=self.user.id)
        )

        event_participant = EventParticipant.objects.create(
            event=event,
            participant=self.user,
            role='organizer',
            confirmed_organizer=True,
            confirmed_participant=True,
        )

        response = self.client.delete(f'/events_participants/{event_participant.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Set user as staff
        self.user.is_staff = True
        self.user.save()
        response = self.client.delete(f'/events_participants/{event_participant.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)