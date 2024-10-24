from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


qid_form_validator = RegexValidator(regex=r"^Q\d+$", message="Field must be in the format \"Q123456789\"")


class Skill(models.Model):
    skill_wikidata_item = models.CharField(
        "Wikidata item associated", 
        max_length=30, default='', unique=True,
        help_text="Wikidata item ID of the skill.",
        validators=[qid_form_validator]
    )
    skill_type = models.ManyToManyField(
        "self", 
        verbose_name="Skill type", symmetrical=False, blank=True,
        help_text="ID of the another skill that this skill is a subtype of."
    )
    skill_date_of_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.skill_wikidata_item