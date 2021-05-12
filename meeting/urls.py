from rest_framework.routers import DefaultRouter

from meeting.views import EventViewSet

routes = [
    (r'event', EventViewSet, 'event')
]


