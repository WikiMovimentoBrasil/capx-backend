from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from skills.models import Skill


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


class AreaOfInterest(models.Model):
    area_name = models.CharField(verbose_name=_("Area name"), max_length=128)

    def __str__(self):
        return self.area_name


class OrganizationType(models.Model):
    type_code = models.CharField(verbose_name=_("Type code"), max_length=20, unique=True)
    type_name = models.CharField(verbose_name=_("Type name"), max_length=140)


class Organization(models.Model):
    organization_name = models.CharField(
        verbose_name=_("Organization name"), 
        max_length=256, unique=True,
        error_messages={"unique": _("There's another organization with that name.")})
    organization_description = models.TextField(
        verbose_name=_("Organization description"), 
        max_length=1024, null=True, blank=True)
    organization_code = models.CharField(
        verbose_name=_("Organization code"), 
        max_length=20, unique=True, 
        error_messages={"unique": _("There's another organization with that code.")})
    organization_website = models.URLField(
        verbose_name=_("Organization website"),
        unique=True, null=True, blank=True,
        error_messages={"unique": _("This website is already used by another organization.")})
    organization_type = models.ForeignKey(OrganizationType, 
        verbose_name=_("Organization type"), on_delete=models.RESTRICT)
    organization_location = models.ManyToManyField(Region, 
        verbose_name=_("Region"),
        related_name="organization_region", blank=True)

    def __str__(self):
        if self.organization_code:
            return self.organization_name + " (" + self.organization_code + ")"
        else:
            return self.organization_name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=100, unique=True, help_text=_("100 characters or fewer"))
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=128, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_groups = models.JSONField(null=True, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class Profile(models.Model):
    PRONOUN = (
        ("he-him", _("He/Him")),
        ("she-her", _("She/Her")),
        ("they-them", _("They/Them"))
    )

    CONTACT_METHOD = (
        ("email", _("Email")),
        ("discussion", _("Discussion page")),
        ("wiki", _("Meta-Wiki talk page")),
        ("telegram", _("Telegram")),
        ("IRC", _("IRC")),
    )

    # PERSONAL INFORMATION
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, editable=False)
    pronoun = models.CharField(verbose_name=_("Pronoun"), max_length=20, choices=PRONOUN, null=True, blank=True)
    profile_image = models.URLField(verbose_name=_("Profile image"), null=True, blank=True)
    display_name = models.CharField(verbose_name=_("Display name"), max_length=387, null=True, blank=True)
    birthday = models.DateField(verbose_name=_("Birthday"), null=True, blank=True)
    about = models.TextField(verbose_name=_("About me"), max_length=2000, null=True, blank=True)

    # SOCIAL MEDIA
    twitter = models.CharField(verbose_name=_("Twitter"), max_length=128, null=True, blank=True)
    facebook = models.CharField(verbose_name=_("Facebook"), max_length=128, null=True, blank=True)
    instagram = models.CharField(verbose_name=_("Instagram"), max_length=128, null=True, blank=True)
    telegram = models.CharField(verbose_name=_("Telegram"), max_length=128, null=True, blank=True)
    github = models.CharField(verbose_name=_("GitHub"), max_length=128, null=True, blank=True)
    irc = models.CharField(verbose_name=_("IRC"), max_length=128, null=True, blank=True)
    wiki_unified = models.CharField(verbose_name=_("Wikimedia user account"), max_length=128, null=True, blank=True)
    wiki_develop = models.CharField(verbose_name=_("Wikimedia developer account"), max_length=128, null=True, blank=True)

    # CONTACT
    contact_method = models.CharField(verbose_name=_("Preferred contact method"), max_length=10,
                                      choices=CONTACT_METHOD, null=True, blank=True)

    # LOCALIZATION
    region = models.ManyToManyField(Region, verbose_name=_("Region"), related_name="user_region", blank=True)
    language = models.ManyToManyField(Language, verbose_name=_("Language"), related_name="user_language", blank=True)
    affiliation = models.ManyToManyField(Organization, verbose_name=_("Affiliation"),
                                         related_name="user_affiliation", blank=True)
    wikimedia_project = models.ManyToManyField(WikimediaProject, verbose_name=_("Wikimedia project"),
                                               related_name="user_wikimedia_project", blank=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest, verbose_name=_("Area of interest"),
                                              related_name="user_area_of_interest", blank=True)

    # SKILLS
    skills_known = models.ManyToManyField(Skill, verbose_name=_("Skill known"), related_name="user_skils", blank=True)
    skills_wanted = models.ManyToManyField(Skill, verbose_name=_("Skill desired"), related_name="user_desired_skils",
                                           blank=True)

    def __str__(self):
        if self.user and self.user.first_name:
            if self.user and self.user.last_name:
                if self.user and self.user.middle_name:
                    return self.user.first_name + " " + self.user.middle_name[0] + ". " + self.user.last_name
                else:
                    return self.user.first_name + " " + self.user.last_name
            else:
                return self.user.first_name
        else:
            return self.user.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
