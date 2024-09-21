from .models import Skill
from .serializers import SkillSerializer, ListSkillSerializer
from rest_framework import status, viewsets, filters
from rest_framework.response import Response


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['skill_wikidata_item']

    #Only staff can create and update skills
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can create skills."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can update skills."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if user is staff
        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can delete skills."},
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
    serializer_class = ListSkillSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        aggregated_data = {}
        for item in serializer.data:
            aggregated_data.update(item)

        return Response(aggregated_data)

    def retrieve(self, request, *args, **kwargs):
        return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SkillByTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer  

    def retrieve(self, request, *args, **kwargs):
        skill_id = self.kwargs.get('pk')
        if not skill_id.isdigit():
            return Response(
                {"detail": "Skill ID must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif skill_id == "0":
            skills = Skill.objects.filter(skill_type__isnull=True)
        else:
            skills = Skill.objects.filter(skill_type=skill_id)
        
        data = {skill.id: str(skill) for skill in skills}
        return Response(data)

    def list(self, request, *args, **kwargs):
        response = {'message': 'Please provide a skill_id to retrieve skills.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)