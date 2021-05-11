from django.shortcuts import render
from rest_framework import viewsets

from location.models import Room
from location.serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()