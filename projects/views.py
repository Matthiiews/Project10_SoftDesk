from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project, Issue, Contributor, Comment
from .permissions import (
    ProjectPermissions
)
from .serializers import (
    ProjectSerializer
)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.filter(contributors__user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        data['author'] = request.user.id

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(
                user=request.user, project=project, role='AUTHOR')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def project_detail(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['author'] = project.author.id

        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(
            'Project successfully deleted.', status=status.HTTP_204_NO_CONTENT)
