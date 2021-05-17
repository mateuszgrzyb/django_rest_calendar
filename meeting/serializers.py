from datetime import timedelta

import pytz
from rest_framework import serializers

from django_rest.serializers import NestingModelSerializer
from meeting.models import Event


class TimezoneAwareDateTimeField(serializers.DateTimeField):
    # TODO:
    #   save datetime in UTC timezone??
    def __init__(self, *args, **kwargs):
        format_ = '%Y-%m-%d %H:%M:%S'
        kwargs |= {
            'format': format_,
            'input_formats': [format_, 'iso-8601'],
        }
        super().__init__(*args, **kwargs)

    def get_timezone(self):
        tz_str = self.context['request'].user.timezone
        return pytz.timezone(tz_str)

    def to_representation(self, value):
        tz = self.get_timezone()
        value = value.astimezone(tz)
        return super().to_representation(value)

    def to_internal_value(self, value):
        tz = self.get_timezone()
        internal_value = super().to_internal_value(value)
        return internal_value.replace(tzinfo=tz)


class EventSerializer(NestingModelSerializer):
    class Meta:
        model = Event
        fields = [
            'url',
            'owner',
            'name',
            'agenda',
            'start',
            'end',
            'location',
            'participants',
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
