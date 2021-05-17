from location.models import Room

from django_rest.serializers import NestingModelSerializer


class RoomSerializer(NestingModelSerializer):
    class Meta:
        model = Room
        fields = [
            'manager',
            'name',
            'address'
        ]
