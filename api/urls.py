from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views.accounts import RegisterView, UserViewSet
from api.views.project import (
    ProjectViewSet, ContributorViewSet,
    IssueViewSet, CommentViewSet,)


app_name = "api"

# Créer un routeur DefaultRouter pour la racine de l'API
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
# Créer des URL comme : api/projets/1/contributeurs/ ou
# api/projets/1/problemes/
project_router = routers.NestedSimpleRouter(
    router, r"projects", lookup="project")
project_router.register(
    r"contributors", ContributorViewSet, basename="project-contributors"
)
project_router.register(r"issues", IssueViewSet, basename="project-issues")

# Créer des URL comme : api/projets/1/problemes/1/commentaires/
comments_router = routers.NestedSimpleRouter(
    project_router, r"issues", lookup="issue")
comments_router.register(
    r"comments", CommentViewSet, basename="issue-comments")


# Inclusion des vues du routeur dans les URLpatterns
urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="Sign_up"),
    path("login/", TokenObtainPairView.as_view(), name="Token obtain pair"),
    path("users/", UserViewSet.as_view({"get": "list"}), name="User list"),
    path("", include(project_router.urls)),
    path("", include(comments_router.urls)),
    path("users/<int:pk>/", UserViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "patch": "update"}
        ),
        name="user-detail",
    ),
]
