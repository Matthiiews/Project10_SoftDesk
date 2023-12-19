from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views.accounts import RegisterView, UserViewSet
# from api.views ProjectViewSet


app_name = "api"

# Create DefaultRouter for API Root
router = routers.DefaultRouter()
# router.register(r'projects', ProjectViewSet, basename='project')


# Inclusion des vues du router dans les URLpatterns
urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="Signup"),
    path("login/", TokenObtainPairView.as_view(), name="Token obtain pair"),
    path("users/", UserViewSet.as_view({"get": "list"}), name="User list"),
    # path("", include(project_router.urls)),
    # path('<int:project_pk>/users/', users.contributor_list),
    # path('', include(router.urls)),
]

# Ajout de format_suffix_patterns pour prendre en charge les suffixes de format
# urlpatterns = format_suffix_patterns(urlpatterns)
