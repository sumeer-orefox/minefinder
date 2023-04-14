from .serializers import ProjectSerializer
from projects.models import Project
from rest_framework import generics

class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer