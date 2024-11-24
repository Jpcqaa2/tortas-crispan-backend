"""Global serializers."""

# Django REST Framework
from rest_framework import serializers

from django.utils.encoding import force_str
from django.db.models import Case, CharField, Value, When


class DataChoiceSerializer(serializers.SerializerMethodField):
    """
    A read-only field that return the representation of a model field with choices.
    """

    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        label = 'get_{field_name}_display'.format(field_name=self.field_name)
        value_choice = '{field_name}'.format(field_name=self.field_name)
        # retrieve instance method
        label = getattr(value, label)
        value_choice = getattr(value, value_choice)
        return {
            'value': value_choice,
            'label': label()
        }


class DataSerializer(serializers.Serializer):
    value = serializers.IntegerField(help_text="ID", read_only=True)
    label = serializers.CharField(help_text="Name", read_only=True)

    def to_representation(self, instance):
        return {
            'value': instance.pk,
            'label': instance.name
        }
    

class WithChoicesSerializer(Case):
    def __init__(self, model, field, field_sub_table=None, condition=None, then=None, **lookups):
        choices = dict(model._meta.get_field(field).flatchoices)
        if field_sub_table is not None:
            field = field_sub_table
        whens = [When(**{field: k, 'then': Value(force_str(v))}) for k, v in choices.items()]
        return super().__init__(*whens, output_field=CharField())