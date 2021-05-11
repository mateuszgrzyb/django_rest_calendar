from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import all_timezones

MAX_TZ_LENGTH = max(len(tz) for tz in all_timezones)
# MAX_TZ_LENGTH = 32


class User(AbstractUser):
    company_id = models.UUIDField(
    )

    timezone = models.CharField(
        choices=((tz, tz) for tz in all_timezones),
        max_length=MAX_TZ_LENGTH,
    )
