from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Skill

@registry.register_document
class SkillDocument(Document):

    class Index:
        name = 'capx_skills'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Skill
        fields = ['skill_name']