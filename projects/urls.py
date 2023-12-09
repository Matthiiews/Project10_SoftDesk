from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    # URL pour la liste des projets
    path('', views.project_list),
    # URL pour les détails d'un projet spécifique
    path('<int:project_pk>/', views.project_detail),
    # URL pour la liste des contributeurs d'un projet spécifique
    path('<int:project_pk>/users/', views.contributor_list),
]

# Ajout de format_suffix_patterns pour prendre en charge les suffixes de format
urlpatterns = format_suffix_patterns(urlpatterns)