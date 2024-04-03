from rest_framework import serializers
from .models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id',
            'skill_name',
            'skill_description',
            'skill_type',
            'skill_wikidata_item',
        ]
