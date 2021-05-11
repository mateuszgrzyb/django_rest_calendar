from django.db import models

from django_rest import settings
from user.models import User


# Create your models here.

class Room(models.Model):
    manager = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=settings.MAX_LENGTH,
    )

    address = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.name

