from django.db.models.base import ModelBase
from rest_framework import serializers

from location.models import Room
from meeting.models import Event
from user.models import User


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        s for c in cls.__subclasses__() for s in all_subclasses(c)
    )


class MyModelSerializerMetaclass(serializers.SerializerMetaclass):
    def __new__(mcs, name, bases, attrs):
        Meta = attrs.get('Meta')
        if Meta is not None and not hasattr(Meta, 'abstract'):
            assert hasattr(Meta, 'model'), f'{name}.Meta needs field "model"'
            assert isinstance(Meta.model, ModelBase), \
                f'{name}.Meta.model should be of type ModelBase'

        return super().__new__(mcs, name, bases, attrs)


class MyModelSerializer(
    serializers.HyperlinkedModelSerializer,
    metaclass=MyModelSerializerMetaclass
):
    @property
    def relations(self):
        # circular dependencies
        from location.serializers import RoomSerializer
        from meeting.serializers import EventSerializer
        from user.serializers import UserSerializer

        # FIXME:
        #   MyModelSerializer.__subclasses__()?
        return {
            Room: RoomSerializer,
            User: UserSerializer,
            Event: EventSerializer,
        }

    # FIXME:
    #   more general, slower????
    # @property
    # def relations(self):
    #     return {
    #         cls.Meta.model: cls
    #         for cls in all_subclasses(MyModelSerializer)
    #         if hasattr(cls, 'Meta')
    #     }

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

        # fix for MyModelSerializer.__subclasses__() hook
        # 1.
        # InnerSerializer.__bases__ = (serializers.HyperlinkedModelSerializer,)
        # 2.
        # import gc
        # gc.collect()

        # print(f'no of MMS subclasses: {len(all_subclasses(MyModelSerializer))}')

        return InnerSerializer, kwargs
