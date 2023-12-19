from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models.project import Project, Issue, Comment
from api.permissions import IsAuthor, IsProjectAuthorOrContributor
from api.serializers.accounts import (
    ContributorSerializer, ContributorDeatilSerializer)
from api.serializers.project import (
    ProjectCreateSerializer, ProjectListSerializer, ProjectDetailSerializer,
    IssueCreateSerializer, IssueListSerializer, IssueDetailSerializer,
    CommentCreateSerializer, CommentListSerializer, CommentDetailSerializer)
from api.views.mixins import SerializerClassMixin

UserModel = get_user_model()


class ProjectViewSet(SerializerClassMixin, ModelViewSet):
    serializer_class = ProjectCreateSerializer
    serializer_create_class = ProjectCreateSerializer
    serializer_detail_class = ProjectDetailSerializer
    serializer_list_class = ProjectListSerializer
    permission_classes = [IsAuthor, IsAuthenticated]
    
    _project = None  # Initialisation de la variable

    @property
    def project(self):
        if self._project is None:
            self._project = Project.objects.filter(
                contributors=self.request.user)
        return self._project
    
    def get_queryset(self):
        # Utilisez order_by pour éviter l'avertissement lié à la pagination
        return self.project.order_by("created_time")
    
    def perform_create(self, serializer):
        # save the author as author and as contributor (request.user)
        serializer.save(
            author=self.request.user, contributors=[self.request.user])
        

class ContributorViewSet(ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing contributors/users
    - The queryset is based on the contributors of a project
    - Display all contributors/Users related to the project mentioned in the
    url.
    """
    
    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorOrContributor]
    
    _project = None  # create this variable to avoid unnecessary database queries
    
    @property
    def project(self):
        """
        Crée un attribut 'project' à l'intérieur de ContributorViewSet.
        Cet attribut est disponible dans la vue et peut être appelé/disponible
        dans le sérialiseur.
        """
        # Si la vue n'a jamais été exécutée auparavant, elle effectuera la
        # requête à la base de données
        # Sinon, _project aura une valeur et aucune requête à la base de
        # données ne sera effectuée
        if self._project is None:
            self._project = get_object_or_404(
                Project.objects.all().prefetch_related("contributors"),
                pk=self.kwargs["project_pk"],
            )
        return self._project
    
    def get_queryset(self):
        # use the UserModel attribute 'date_joined' to order to avoid the
        # pagination warning
        return self.project.contributors.all().order_by("date_joined")
    