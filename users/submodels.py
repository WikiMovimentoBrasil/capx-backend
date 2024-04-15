from django.db import models
from django.utils.translation import gettext_lazy as _

class Region(models.Model):
    region_name = models.CharField(verbose_name=_("Region name"), max_length=128, unique=True)
    parent_region = models.ManyToManyField("self", verbose_name=_("Parent region"), symmetrical=False,
                                           related_name="region_parent", blank=True)

    def __str__(self):
        return self.region_name


class Language(models.Model):
    language_name = models.CharField(verbose_name=_("Language name"), max_length=128)
    language_code = models.CharField(verbose_name=_("Language code"), max_length=10, unique=True)

    def __str__(self):
        return self.language_name


class WikimediaProject(models.Model):
    wikimedia_project_name = models.CharField(verbose_name=_("Wikimedia project name"), max_length=128)
    wikimedia_project_code = models.CharField(verbose_name=_("Wikimedia project code"), max_length=40, unique=True)

    def __str__(self):
        return self.wikimedia_project_name