from rest_framework.metadata import SimpleMetadata
from rest_framework.serializers import ManyRelatedField
from django.utils.encoding import force_str


class CustomMetadata(SimpleMetadata):

    def get_field_info(self, field):
        field_info = super().get_field_info(field)

        if (not field_info.get('read_only') and
            isinstance(field, ManyRelatedField) and
                 hasattr(field, 'choices')):
            field_info['choices'] = [
                {
                    'value': choice_value,
                    'display_name': force_str(choice_name, strings_only=True)
                }
                for choice_value, choice_name in field.choices.items()
            ]
 
        return field_info