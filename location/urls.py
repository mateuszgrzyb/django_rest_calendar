from rest_framework.routers import DefaultRouter

from location.views import RoomViewSet

routes = [
    (r'room', RoomViewSet)
]
