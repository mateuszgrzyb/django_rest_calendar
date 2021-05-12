from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import all_timezones
from django.utils.translation import gettext_lazy as _

MAX_TZ_LENGTH = max(len(tz) for tz in all_timezones)


# MAX_TZ_LENGTH = 32


class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGER = 'M', _('Manager')
        OWNER = 'O', _('Owner')
        PARTICIPANT = 'P', _('Participant')
        ADMIN = 'A', _('Administrator')

    role = models.CharField(
        max_length=1,
        choices=Role.choices,
    )

    company_id = models.UUIDField(
    )

    timezone = models.CharField(
        choices=((tz, tz) for tz in all_timezones),
        max_length=MAX_TZ_LENGTH,
        null=False,
        blank=False,
    )


class Manager(models.Model):
    profile = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    def __str__(self):
        return self.profile.username


class Owner(models.Model):
    profile = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    def __str__(self):
        return self.profile.username


class Participant(models.Model):
    profile = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    def __str__(self):
        return self.profile.username

