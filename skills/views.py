from .models import Skill
from .serializers import SkillSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

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
