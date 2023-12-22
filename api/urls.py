from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views.accounts import RegisterView, UserViewSet
from api.views.project import (
    ProjectViewSet, ContributorViewSet,
    IssueViewSet, CommentViewSet,)


app_name = "api"

# Create DefaultRouter for API Root
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
# create url like: api/projects/1/contributors/ or api/projects/1/issues/
project_router = routers.NestedSimpleRouter(
    router, r"projects", lookup="project")
project_router.register(
    r"contributors", ContributorViewSet, basename="project-contributors"
)
project_router.register(r"issues", IssueViewSet, basename="project-issues")

# create url like: api/projects/1/issues/1/comments/
comments_router = routers.NestedSimpleRouter(
    project_router, r"issues", lookup="issue")
comments_router.register(
    r"comments", CommentViewSet, basename="issue-comments")


# Inclusion des vues du router dans les URLpatterns
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
