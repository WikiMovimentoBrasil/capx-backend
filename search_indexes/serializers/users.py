from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents.users import ProfileDocument

class UsersDocumentSerializer(DocumentSerializer):

    class Meta:
        document = ProfileDocument
        fields = [
            'id',
            'user__username',
            'display_name',
            'about',
        ]