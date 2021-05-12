from rest_framework import serializers
from rest_framework.serializers import SerializerMetaclass

from django_rest.serializers import MyModelSerializerMetaclass, MyModelSerializer
from location.models import Room




class RoomSerializer(
    MyModelSerializer
    # serializers.ModelSerializer,
    # metaclass=MyModelSerializerMetaclass
):
    class Meta:
        model = Room
        fields = '__all__'

    # url = None

