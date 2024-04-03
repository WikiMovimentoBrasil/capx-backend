from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from .models import Skill
from .serializers import SkillSerializer
from rest_framework.views import APIView


class SkillAPIView(APIView):

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SkillDetails(APIView):

    def get_object(self, id):
        try:
            return Skill.objects.get(id=id)
        except Skill.DoesNotExist:
            raise Http404

    def get(self, request, id):
        skill = self.get_object(id)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    def put(self, request, id):
        skill = self.get_object(id)
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        skill = self.get_object(id)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
