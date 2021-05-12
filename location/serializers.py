from location.models import Room

from django_rest.serializers import MyModelSerializer


class RoomSerializer(MyModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
