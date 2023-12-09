from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


rlpatterns = [
    path('', views.project_list),
    path('<int:project_pk>/', views.project_detail),
    path('<int:project_pk>/users/', views.contributor_list),
]