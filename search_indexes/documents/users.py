from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from users.models import Profile

INDEX = Index('profiles')
INDEX.settings(
    number_of_shards=1, 
    number_of_replicas=1
)

@INDEX.doc_type
class ProfileDocument(Document):
    user = fields.ObjectField(properties={
        'username': fields.TextField(),
    })
    display_name = fields.TextField(),
    about = fields.TextField(),
    id = fields.IntegerField(attr='id'),

    class Django:
        model = Profile