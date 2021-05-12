import datetime
import re
import pytz
from django.db.models import Q

from rest_framework import viewsets

from meeting.models import Event
from meeting.serializers import EventSerializer, NestedEventSerializer

from meeting.exceptions import QueryParamError


def day_selector(day, tz):
    print('day')
    day_regex = re.compile(r"\d{4}-\d{2}-\d{2}")

    if day_regex.fullmatch(day) is None:
        raise QueryParamError()

    try:
        day = datetime.date(*map(int, day.split('-')))
    except ValueError as ve:
        raise QueryParamError() from ve

    day_start = datetime.datetime.combine(day, datetime.time.min, tzinfo=tz)
    day_end = datetime.datetime.combine(day, datetime.time.max, tzinfo=tz)
    return Q(start__range=(day_start, day_end))


def location_selector(location_id):
    print('location')
    return Q(location_id=location_id)


def query_selector(query):
    print('query')
    return Q(name__contains=query) | Q(agenda__contains=query)


def q_or_fun(fun, val, *args):
    return Q() if val is None else fun(*((val,) + args))


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.nested:
            return NestedEventSerializer
        else:
            return EventSerializer

    def get_queryset(self):
        self.nested = False
        tz = pytz.timezone(self.request.user.timezone)
        query_dict = self.request.query_params

        if query_dict.get('nested') is not None:
            self.nested = True

        return Event.objects.filter(
            q_or_fun(day_selector, query_dict.get('date'), tz) &
            q_or_fun(location_selector, query_dict.get('location_id')) &
            q_or_fun(query_selector, query_dict.get('query'))
        )
