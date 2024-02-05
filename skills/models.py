from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone


qid_form_validator = RegexValidator(regex=r"^Q\d+$", message=_("Field must be in the format \"Q123456789\""))


class Skill(models.Model):
    skill_name = models.CharField(_("Name"), max_length=128)
    skill_description = models.CharField(_("Description"), max_length=1000)
    skill_type = models.ManyToManyField("self", verbose_name=_("Skill type"), symmetrical=False, blank=True)
    skill_wikidata_item = models.CharField(_("Wikidata item associated"), max_length=30, null=True, blank=True, validators=[qid_form_validator])
    skill_date_of_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.skill_name