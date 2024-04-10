from .models import Skill
from .serializers import SkillSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if this skill is referenced by any other item's skill_type
        if Skill.objects.filter(skill_type=instance).exists():
            return Response(
                {"detail": "This skill is referenced by other items and cannot be deleted."},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
