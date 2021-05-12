from rest_framework import serializers

from location.models import Room


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        # fields = '__all__'
        exclude = ['manager']

    # manager = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
