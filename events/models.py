from django.db import models
from users.models import Profile, CustomUser
from django.conf import settings
from orgs.models import Organization
from django.core.validators import RegexValidator


class Events(models.Model):
    LOCATION_TYPES = [
        ("virtual", "Virtual"),
        ("in_person", "In Person"),
        ("hybrid", "Hybrid"),
    ]
    name = models.CharField(max_length=128, verbose_name="Event Name")
    type_of_location = models.CharField(choices=LOCATION_TYPES, max_length=20, verbose_name="Type of Location")
    openstreetmap_id = models.URLField(blank=True, verbose_name="OpenStreetMap ID", validators=[RegexValidator(
        regex=r'^https://www.openstreetmap.org/(node|way|relation)/\d+$',
        message="Invalid OpenStreetMap ID format. The format should be https://www.openstreetmap.org/(way|node|relation)/12345"
    )])
    url = models.URLField(blank=True, verbose_name="Event URL")
    wikidata_qid = models.CharField(max_length=10, blank=True, verbose_name="Wikidata Qid", validators=[RegexValidator(
        regex=r'^Q[1-9]\d*$',
        message="Invalid Wikidata Qid format. The format should be Q12345"
    )])
    time_begin = models.DateTimeField(verbose_name="Start Time")
    time_end = models.DateTimeField(verbose_name="End Time")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name="events_created", verbose_name="Event Creator")
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, through="EventParticipant", related_name="team_members", verbose_name="Event Team")
    organizations = models.ManyToManyField(Organization, through="EventOrganizations", verbose_name="Event Organizations")
    related_skills = models.ManyToManyField("skills.Skill", blank=True, verbose_name="Related Skills")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name
    
class EventParticipant(models.Model):
    ROLE_TYPES = [
        ("organizer", "Organizer"),
        ("committee", "Committee"),
        ("volunteer", "Volunteer"),
    ]
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    role = models.CharField(choices=ROLE_TYPES, max_length=20)
    confirmed_organizer = models.BooleanField(default=False)
    confirmed_participant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.participant} - {self.event}"
    
class EventOrganizations(models.Model):
    ROLE_TYPES = [
        ("organizer", "Organizer"),
        ("sponsor", "Sponsor"),
        ("supporter", "Supporter"),
    ]
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.RESTRICT)
    role = models.CharField(choices=ROLE_TYPES, max_length=20)
    confirmed_organizer = models.BooleanField(default=False)
    confirmed_organization = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.organization} - {self.event}"