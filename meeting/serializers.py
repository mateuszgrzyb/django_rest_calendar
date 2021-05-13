from datetime import timedelta

import pytz
from rest_framework import serializers
from rest_framework.settings import api_settings

from django_rest.serializers import MyModelSerializer
from meeting.models import Event


class TimezoneAwareDateTimeField(serializers.DateTimeField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        tz = self.context['request'].user.timezone
        value = value.replace(tzinfo=pytz.timezone(tz))
        return super().to_representation(value)


class EventSerializer(
    # serializers.HyperlinkedModelSerializer
    MyModelSerializer
):
    class Meta:
        model = Event
        # exclude = ['participants']
        fields = [
            'url',
            'owner',
            'name',
            'agenda',
            'start',
            'end',
            'location',
        ]

    start = TimezoneAwareDateTimeField(
    )

    end = TimezoneAwareDateTimeField(
    )

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        valid = super().validate(attrs)
        start, end = valid['start'], valid['end']
        if (start + timedelta(hours=8)) < end or start >= end:
            raise serializers.ValidationError("Event time must be positive and lower than 8h")
        return valid


class NestedEventSerializer(EventSerializer):
    class Meta(EventSerializer.Meta):
        depth = 1
