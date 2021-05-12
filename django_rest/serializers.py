from rest_framework import serializers

from location.models import Room
from meeting.models import Event
from user.models import User


class MyModelSerializer(serializers.HyperlinkedModelSerializer):

    #
    @property
    def relations(self):
        # circular dependencies
        from location.serializers import RoomSerializer
        from meeting.serializers import EventSerializer
        from user.serializers import UserSerializer
        return {
            Room: RoomSerializer,
            User: UserSerializer,
            Event: EventSerializer,
        }

    def build_nested_field(self, field_name, relation_info, nested_depth):
        _, kwargs = \
            super().build_nested_field(field_name, relation_info, nested_depth)

        class DefaultSerializer(serializers.ModelSerializer):
            class Meta:
                model = relation_info.related_model
                fields = '__all__'

        field_class = self.relations.get(
            relation_info.related_model,
            DefaultSerializer,
        )

        class InnerSerializer(field_class):
            class Meta(field_class.Meta):
                depth = nested_depth - 1

        return InnerSerializer, kwargs

