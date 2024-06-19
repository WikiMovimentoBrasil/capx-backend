from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from orgs.models import Organization
from skills.models import Skill
from users.submodels import Territory, Language, WikimediaProject
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        "Username",
        max_length=100,
        unique=True
    )
    email = models.EmailField(
        "Email address",
        max_length=255,
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(
        "Staff status",
        default=False
    )
    is_active = models.BooleanField(
        "Active",
        default=True
    )
    date_joined = models.DateTimeField(
        "Date joined",
        default=timezone.now
    )
    user_groups = models.JSONField(
        null=True,
        blank=False
    )

    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'


class Profile(models.Model):
    PRONOUNS = (
        ("he-him", "He/Him"),
        ("she-her", "She/Her"),
        ("they-them", "They/Them"),
        ("not-specified", "Not specified"),
        ("other", "Other")
    )
    CONTACT_METHODS = (
        ("email", "Email"),
        ("discussion", "Discussion page"),
        ("wiki", "Meta-Wiki talk page"),
        ("IRC", "IRC"),
    )

    # PERSONAL INFORMATION
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        editable=False
    )
    profile_image = models.URLField(
        verbose_name="Profile image",
        null=True,
        blank=True
    )
    display_name = models.CharField(
        verbose_name="Display name",
        max_length=387,
        blank=True
    )
    pronoun = models.CharField(
        verbose_name="Pronoun",
        max_length=20,
        choices=PRONOUNS,
        blank=True
    )
    about = models.TextField(
        verbose_name="Short bio",
        max_length=2000,
        blank=True,
        default=""
    )
    wikidata_qid = models.CharField(
        verbose_name="Wikidata Qid",
        max_length=10,
        blank=True,
        validators=[RegexValidator(
            regex=r'^Q[1-9]\d*$',
            message="Invalid Wikidata Qid format. The format should be Q12345"
        )]
    )
    wiki_alt = models.CharField(
        verbose_name="Wikimedia alternative account",
        max_length=128,
        blank=True
    )

    # COMMUNITY
    territory = models.ManyToManyField(
        Territory,
        verbose_name="Territory",
        related_name="user_territory",
        blank=True)
    language = models.ManyToManyField(
        Language,
        verbose_name="Language",
        related_name="user_language",
        blank=True
    )
    affiliation = models.ManyToManyField(
        Organization,
        verbose_name="Affiliation",
        related_name="user_affiliation",
        blank=True
    )
    wikimedia_project = models.ManyToManyField(
        WikimediaProject,
        verbose_name="Wikimedia project",
        related_name="user_wikimedia_project",
        blank=True
    )
    team = models.CharField(
        verbose_name="Team",
        max_length=128,
        blank=True
    )

    # SKILLS
    skills_known = models.ManyToManyField(
        Skill,
        verbose_name="Known capacity",
        related_name="user_known_skils",
        blank=True
    )
    skills_available = models.ManyToManyField(
        Skill,
        verbose_name="Available capacity",
        related_name="user_available_skills",
        blank=True
    )
    skills_wanted = models.ManyToManyField(
        Skill, 
        verbose_name="Wanted capacity", 
        related_name="user_desired_skils",
        blank=True
    )
    
    # CONTACT
    contact = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name="Contact methods", 
        help_text="json"
    )
    social = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name="Social medias", 
        help_text="json"
    )

    def __str__(self):
        return self.user.username

    @property
    def users_indexing(self):
        return {
            'id': self.id,
            'username': self.user.username,
            'display_name': self.display_name,
            'about': self.about,
        }


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
