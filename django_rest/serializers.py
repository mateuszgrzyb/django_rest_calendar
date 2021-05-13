from django.db.models.base import ModelBase
from rest_framework import serializers

from location.models import Room
from meeting.models import Event
from user.models import User


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
    # FIXME: metaclass=MyModelSerializerMetaclass
):
    def get_default_nested_serialier(self):
        return serializers.ModelSerializer

    @property
    def relations(self):
        # circular dependencies
        from location.serializers import RoomSerializer
        from meeting.serializers import EventSerializer
        from user.serializers import UserSerializer

        # FIXME:
        #   MyModelSerializer.__subclasses__()?
        #   Explicit is better than implicit?
        return {
            Room: RoomSerializer,
            User: UserSerializer,
            Event: EventSerializer,
        }

    # FIXME:
    #   more general, slower????
    #   @property
    #   def relations(self):
    #       return {
    #           cls.Meta.model: cls
    #           for cls in all_subclasses(MyModelSerializer)
    #           if hasattr(cls, 'Meta')
    #       }

    def build_nested_field(self, field_name, relation_info, nested_depth):
        _, kwargs = \
            super().build_nested_field(field_name, relation_info, nested_depth)

        class DefaultSerializer(
            self.get_default_nested_serialier()
            # serializers.ModelSerializer
        ):
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

        # FIXME for MyModelSerializer.__subclasses__() hook
        #   1. Disconnects InnerSerializer from MyModelSerializer explicitly
        #   InnerSerializer.__bases__ = (serializers.HyperlinkedModelSerializer,)
        #   2. InnerSerializer is connected to MyModelSerializer by weak reference,
        #      so it can be garbage collected
        #   import gc
        #   gc.collect()

        # print(f'no of MMS subclasses: {len(all_subclasses(MyModelSerializer))}')

        return InnerSerializer, kwargs
