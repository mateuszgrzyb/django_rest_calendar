import abc

from rest_framework import serializers
from django.db import models

def check_if_exists_and_not_null(attrs, attr, val):
    if attr not in attrs.keys():
        attrs[attr] = val

class MyModelSerializerMetaclass(serializers.SerializerMetaclass):
    def __new__(mcs, name, bases, attrs):
        if 'Meta' in attrs.keys() and hasattr(Meta := attrs['Meta'], 'model'):
            view_name = f'{Meta.model.__name__.lower()}-detail'
            if 'url' not in attrs.keys():
                attrs['url'] = serializers.HyperlinkedIdentityField(
                    view_name=view_name
                )
        return super(MyModelSerializerMetaclass, mcs).__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, **kwargs):
        super(MyModelSerializerMetaclass, cls).__init__(name, bases, attrs, **kwargs)


class MyModelSerializer(
    serializers.ModelSerializer,
    metaclass=MyModelSerializerMetaclass,
):

    def build_nested_field(self, field_name, relation_info, nested_depth):
        assert all(
            (hasattr(cls, 'Meta') and hasattr(cls.Meta, 'model'))
            for cls in MyModelSerializer.__subclasses__()
        ), 'All subclasses of this serializer has to have Meta.model of instance django.db.models.Model'
        print({cls.__name__: hasattr(cls, 'Meta') for cls in MyModelSerializer.__subclasses__()})

        default_field_class, field_kwargs = \
            super().build_nested_field(field_name, relation_info, nested_depth)
        field_class = {
            cls.Meta.model: cls for cls in MyModelSerializer.__subclasses__()
        }.get(relation_info.related_model, default_field_class)
        return field_class, field_kwargs
