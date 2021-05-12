from django.shortcuts import render
from rest_framework import viewsets

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
