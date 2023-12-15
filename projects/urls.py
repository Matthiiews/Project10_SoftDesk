from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

# from .views import ProjectViewSet, ContributorViewSet
from . import views


# Création d'un routeur
# router = DefaultRouter()
# router.register(r'projects', ProjectViewSet, basename='project')
# router.register(r'contributors', ContributorViewSet, basename='contributor')

# Inclusion des vues du router dans les URLpatterns
urlpatterns = [
    path('', views.project_list),
    path('<int:project_pk>/', views.project_detail),
    path('<int:project_pk>/users/', views.contributor_list),
    # path('', include(router.urls)),
]

# Ajout de format_suffix_patterns pour prendre en charge les suffixes de format
urlpatterns = format_suffix_patterns(urlpatterns)
