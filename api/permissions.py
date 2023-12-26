from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Project


class IsAuthor(BasePermission):
    """
    Permission au niveau de l'objet permettant uniquement aux objets ayant des
    auteurs obj.auteurs de les éditer et de les supprimer.
    """

    message = "You have to be the author to update or delete."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsProjectAuthorOrContributor(BasePermission):
    """
    Permission au niveau de l'objet permettant uniquement aux auteurs de
    modifier et supprimer un objet
    - permission spéciale pour ContributorViewSet
    """

    message = "You have to be the author to update or delete."

    def has_permission(self, request, view):
        # Autoriser les méthodes sûres (GET et POST)
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)

        # Vérifier si request.user est un contributeur
        if request.user in project.contributors.all():
            return True

        # Autoriser la modification uniquement par l'auteur du projet
        return request.user == project.author

    def has_object_permission(self, request, view, obj):
        # GET, POST, PUT, PATCH, DELETE with pk
        if request.method in SAFE_METHODS:
            return True

        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)
        return project.author == request.user


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return True  # Autoriser toutes les requêtes à passer la vérification
        # initiale des permissions

    def has_object_permission(self, request, view, obj):
        # Refuser l'action sur les objets si l'utilisateur n'est pas
        # authentifié
        if not request.user.is_authenticated:
            return False

        if view.action in ["retrieve", "update", "partial_update"]:
            return (
                obj == request.user
            )  # Autoriser l'utilisateur à récupérer, mettre à jour ou
            # partiellement mettre à jour ses propres données
        else:
            return False  # Pour les autres actions, refuser toutes les
            # requêtes
