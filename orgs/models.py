from django.db import models
from users.submodels import Region
from django.core.validators import RegexValidator
from django.utils import timezone as timezone


class OrganizationType(models.Model):
    type_code = models.CharField(max_length=20, unique=True)
    type_name = models.CharField(max_length=140)

    def __str__(self):
        return self.type_name


class Organization(models.Model):
    display_name = models.CharField(max_length=255)
    profile_image = models.URLField(blank=True, null=True, validators=[RegexValidator(
        regex=r'^https:\/\/commons\.wikimedia\.org\/wiki\/File:.*?\.[\w]+$',
        message='Invalid URL format. The format should be https://commons.wikimedia.org/wiki/File:filename.ext'
    )])
    acronym = models.CharField(max_length=10, unique=True)
    type = models.ForeignKey(OrganizationType, on_delete=models.RESTRICT)
    territory = models.ManyToManyField(Region)
    managers = models.ManyToManyField('users.CustomUser', related_name='managers')
    social_media = models.URLField(blank=True, null=True)
    home_project = models.URLField(blank=True, null=True)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.acronym:
            return self.display_name + " (" + self.acronym + ")"
        else:
            return self.display_name
