from rest_framework.metadata import SimpleMetadata
from rest_framework.serializers import ManyRelatedField
from django.utils.encoding import force_str


class CustomMetadata(SimpleMetadata):
    """
    Custom metadata class that extends the SimpleMetadata class.

    This class overrides the get_field_info method to provide choices to ManyRelatedField
    instances temporarily on the OPTIONS method of the Django REST Framework (DRF).
    This is done until a better method for providing choices is established.

    """

    def get_field_info(self, field):
        """
        Get the metadata information for a given field.

        Args:
            field: The field for which to retrieve the metadata information.

        Returns:
            dict: The metadata information for the given field.

        """
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