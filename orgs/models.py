from django.db import models
from users.models import Region
from django.utils import timezone
from django.core.validators import RegexValidator


class Organization(models.Model):
    display_name = models.CharField(max_length=255)
    profile_image = models.URLField(blank=True, null=True, validators=[RegexValidator(
        regex=r'^https:\/\/commons\.wikimedia\.org\/wiki\/File:.*?\.[\w]+$',
        message='Invalid URL format. The format should be https://commons.wikimedia.org/wiki/File:filename.ext'
    )])
    acronym = models.CharField(max_length=10, unique=True)
    territory = models.ManyToManyField(Region)
    contact = models.CharField(max_length=255, blank=True, null=True)
    social_media = models.URLField(blank=True, null=True)
    home_project = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    