from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import all_timezones
from django.utils.translation import gettext_lazy as _

from django_rest.misc import all_subclasses

MAX_TZ_LENGTH = max(len(tz) for tz in all_timezones)


# MAX_TZ_LENGTH = 32

class Role(models.Model):
    class Meta:
        abstract = True

    profile = models.OneToOneField(
        to='User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.profile.username


class Manager(Role):
    pass


class Owner(Role):
    pass


class Participant(Role):
    pass


class Administrator(Role):
    pass


# User class has to be at the bottom
class User(AbstractUser):
    class RoleError(Exception):
        pass

    roles = {cls.__name__: cls for cls in all_subclasses(Role)}
    role_names = [(n, _(n)) for n in roles.keys()]

    role_name = models.CharField(
        max_length=20,
        choices=role_names,
    )

    def get_role(self, role_name):
        try:
            return self.roles[role_name].objects.get(profile=self)
        except KeyError as ke:
            raise User.RoleError(f'{role_name} does not exist') from ke

        # TODO:
        #   try:
        #       return getattr(self, role_name)
        #   except AttributeError as ae
        #       raise User.RoleError(f'{role_name} does not exist') from ae

    company_id = models.UUIDField(
    )

    timezone = models.CharField(
        choices=((tz, tz) for tz in all_timezones),
        max_length=MAX_TZ_LENGTH,
        null=False,
        blank=False,
    )
