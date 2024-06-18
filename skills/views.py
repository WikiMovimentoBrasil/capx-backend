from .models import Skill
from .serializers import SkillSerializer
from rest_framework import status, viewsets, filters
from rest_framework.response import Response


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['skill_wikidata_item']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if user is staff
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if this skill is referenced by any other item's skill_type
        if Skill.objects.filter(skill_type=instance).exists():
            return Response(
                {"detail": "This skill is referenced by other items and cannot be deleted."},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSkillViewSet (viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {skill.id: str(skill) for skill in queryset}
        return Response(data)