from django.test import TestCase
from rest_framework.serializers import CharField, ChoiceField
from rest_framework.metadata import SimpleMetadata
from CapX.metadata import CustomMetadata


class CustomMetadataTestCase(TestCase):
    def setUp(self):
        self.metadata = CustomMetadata()
        self.field = CharField()
        self.choice_field = ChoiceField(choices=[('1', 'One'), ('2', 'Two')])

    def test_get_field_info(self):
        field_info = self.metadata.get_field_info(self.field)
        self.assertEqual(field_info, SimpleMetadata().get_field_info(self.field))

    def test_get_field_info_with_choices(self):
        field_info = self.metadata.get_field_info(self.choice_field)
        expected_choices = [
            {'value': '1', 'display_name': 'One'},
            {'value': '2', 'display_name': 'Two'}
        ]
        self.assertEqual(field_info['choices'], expected_choices)