from datetime import datetime, timedelta

from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from django_rest import settings
from user.models import User
from location.models import Room


class Event(models.Model):
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='organized_event_set',
    )

    name = models.CharField(
        max_length=settings.MAX_LENGTH
    )

    agenda = models.TextField()

    start = models.DateTimeField()

    end = models.DateTimeField()

    participants = models.ManyToManyField(
        to=User,
        related_name='participated_event_set',
    )

    location = models.ForeignKey(
        to=Room,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    # alternative solution to serializer validation
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             name="Event's 8h time limit",
    #             check=Q(end__lt=(F('start')+timedelta(hours=8))) & Q(end__gt=F('start'))
    #         )
    #     ]

    def __str__(self):
        return self.name