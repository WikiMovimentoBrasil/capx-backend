from django.db import models
from users.models import Region
from django.utils import timezone


class Organization(models.Model):
    display_name = models.CharField(max_length=255)
    profile_image = models.URLField()
    acronym = models.CharField(max_length=10, unique=True)
    territory = models.ManyToManyField(Region)
    contact = models.CharField(max_length=255)
    social_media = models.URLField()
    home_project = models.URLField()
    creation_date = models.DateTimeField(default=timezone.now)

    