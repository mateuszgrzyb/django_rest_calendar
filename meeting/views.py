import datetime
import re

import pytz
from django.shortcuts import render
from rest_framework import viewsets, permissions

from meeting.models import Event
from meeting.serializers import EventSerializer, NestedEventSerializer


def filter_events_by_day(queryset, day, tz):
    day_start = datetime.datetime.combine(day, datetime.time.min, tzinfo=tz)
    day_end = datetime.datetime.combine(day, datetime.time.max, tzinfo=tz)
    return queryset.filter(start__range=(day_start, day_end))


class EventViewSet(viewsets.ModelViewSet):
    nested = False
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.nested:
            return NestedEventSerializer
        else:
            return EventSerializer

    # TODO:
    #   CLEAN UP
    def get_queryset(self):
        type(self).nested = False
        queryset = super().get_queryset()
        # change it
        # get it from user model
        tz = pytz.UTC
        day_regex = re.compile(r'\d{4}-\d{2}-\d{2}')

        query_dict = self.request.query_params
        query_keys = query_dict.keys()

        print({k: query_dict[k] for k in query_keys})

        if ((val := query_dict.get('day')) is not None
                and day_regex.fullmatch(val) is not None):
            day = datetime.date(*map(int, val.split('-')))
            queryset = filter_events_by_day(super().get_queryset(), day, tz)

        if query_dict.get('nested') is not None:
            type(self).nested = True
            queryset = super().get_queryset()

        return queryset
