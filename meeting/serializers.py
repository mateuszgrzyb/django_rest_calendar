from datetime import timedelta

from rest_framework import serializers

from meeting.models import Event
from django_rest.serializers import MyModelSerializerMetaclass, MyModelSerializer


class EventSerializer(
    MyModelSerializer,
    # serializers.ModelSerializer,
    # metaclass=MyModelSerializerMetaclass,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Event
        exclude = ['participants']

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

