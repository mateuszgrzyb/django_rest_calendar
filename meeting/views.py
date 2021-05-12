import datetime
import re
import pytz

from rest_framework import viewsets

from meeting.models import Event
from meeting.serializers import EventSerializer, NestedEventSerializer

from meeting.exceptions import QueryParamError


def filter_events_by_day(queryset, day, tz):
    day_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
    #day_regex = re.compile(r"\d{4}-[1-9]|1[0-2]-[1-9]|[1-2][0-9]|30|31")

    if day_regex.fullmatch(day) is None:
        raise QueryParamError()

    day = datetime.date(*map(int, day.split('-')))

    day_start = datetime.datetime.combine(day, datetime.time.min, tzinfo=tz)
    day_end = datetime.datetime.combine(day, datetime.time.max, tzinfo=tz)
    return queryset.filter(start__range=(day_start, day_end))


def filter_events_by_location(queryset, location_id):
    return queryset.filter(location_id=location_id)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.nested:
            return NestedEventSerializer
        else:
            return EventSerializer

    # TODO:
    #   CLEAN UP
    def get_queryset(self):
        self.nested = False

        # change it - get it from user model
        tz = pytz.UTC

        query_dict = self.request.query_params
        query_keys = query_dict.keys()

        # print({k: query_dict[k] for k in query_keys})

        if query_dict.get('nested') is not None:
            self.nested = True

        queryset = Event.objects.all()

        if (day := query_dict.get('day')) is not None:
            queryset = filter_events_by_day(queryset, day, tz)

        if (location_id := query_dict.get('location_id')) is not None:
            queryset = filter_events_by_location(queryset, location_id)

        return queryset

