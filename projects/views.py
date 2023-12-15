from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project, Contributor, Issue, Comment
from .permissions import (
    ProjectPermissions,
    ContributorPermissions,
)
from .serializers import (
    ProjectSerializer,
    ContributorSerializer
)


@api_view(['GET', 'POST'])

def project_list(request):
    """
    API view for listing and creating projects.

    GET: Retrieve a list of projects the user is a contributor to.
    POST: Create a new project with the authenticated user as the author.

    Returns:
        Response: JSON response with project data or validation errors.
    """
    if request.method == 'GET':
        # projects = Project.objects.filter(contributors__user=request.user)
        projects = Project.objects.all()
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



def project_detail(request, project_pk):
    """
    API view for listing and creating contributors for a project.

    GET: Retrieve a list of contributors for a specific project.
    POST: Add a new contributor to the project.

    Returns:
        Response: JSON response with contributor data or validation errors.
    """
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ContributorPermissions])
def contributor_list(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)

    if request.method == 'GET':
        contributors = Contributor.objects.filter(project=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        data['project'] = project.id

        try:
            Contributor.objects.get(user=data['user'], project=project.id)
            return Response(
                'This user has already been added.',
                status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=data['user'])
                serializer = ContributorSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response('This user does not exist.',
                                status=status.HTTP_400_BAD_REQUEST)
