from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


qid_form_validator = RegexValidator(regex=r"^Q\d+$", message="Field must be in the format \"Q123456789\"")


class Skill(models.Model):
    skill_name = models.CharField("Name", max_length=128)
    skill_description = models.CharField("Description", max_length=1000)
    skill_type = models.ManyToManyField("self", verbose_name="Skill type", symmetrical=False, blank=True)
    skill_wikidata_item = models.CharField("Wikidata item associated", max_length=30, default='', blank=True, validators=[qid_form_validator])
    skill_date_of_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.skill_name