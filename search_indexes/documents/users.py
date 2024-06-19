from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from users.models import Profile
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

INDEX = Index('profiles')
INDEX.settings(
    number_of_shards=1, 
    number_of_replicas=1
)

@INDEX.doc_type
class ProfileDocument(Document):
    id = fields.IntegerField(attr='id')
    user = fields.ObjectField(properties={
        'username': StringField(
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
            }
        )
    })
    display_name = StringField(
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    about = StringField()
    

    class Django:
        model = Profile