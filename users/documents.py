from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from .models import Profile

@registry.register_document
class ProfileDocument(Document):
    user = fields.ObjectField(properties={
        'username': fields.TextField()
    })

    class Index:
        name = 'capx_profile'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Profile
        fields = []