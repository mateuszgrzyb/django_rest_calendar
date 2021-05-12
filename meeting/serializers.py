from datetime import timedelta
from rest_framework import serializers

from location.models import Room
from location.serializers import RoomSerializer
from meeting.models import Event
from user.models import User
from user.serializers import UserSerializer


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        exclude = ['participants']

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        valid = super().validate(attrs)
        start, end = valid['start'], valid['end']
        if (start + timedelta(hours=8)) < end or start >= end:
            raise serializers.ValidationError("Event time must be positive and lower than 8h")
        return valid

    # def create(self, validated_data):
    #     try:
    #         result = super().create(validated_data)
    #     except IntegrityError as ie:
    #         # not the best way, but I believe it's the shortest one
    #         # also I could've put all of this validation inside self.validate method
    #         raise serializers.ValidationError(str(ie))
    #     return result

    def build_nested_field(self, field_name, relation_info, nested_depth):
        default_field_class, field_kwargs = \
            super().build_nested_field(field_name, relation_info, nested_depth)

        # TODO:
        #   hardcoded values are never good option, but there shouldn't be any crashes
        #   further testing required
        #   clean up
        print(relation_info.related_model)
        field_class = {
            Room: RoomSerializer,
            User: UserSerializer,
        }.get(relation_info.related_model, default_field_class)

        # if relation_info.related_model is Room:
        #     field_class = RoomSerializer
        # elif relation_info.related_model is User:
        #     field_class = UserSerializer
        # else:
        #     field_class = default_field_class

        return field_class, field_kwargs


class NestedEventSerializer(EventSerializer):
    class Meta(EventSerializer.Meta):
        depth = 1
