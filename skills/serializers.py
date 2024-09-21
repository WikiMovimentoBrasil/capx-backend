from rest_framework import serializers
from .models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id',
            'skill_wikidata_item',
            'skill_type',
        ]

class ListSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id',
            'skill_wikidata_item',
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {data['id']: data['skill_wikidata_item']}
