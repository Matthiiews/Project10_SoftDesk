from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views


urlpatterns = [
    # URL pour l'inscription d'un utilisateur
    path('signup/', views.SignupView.as_view(), name='signup'),
    # URL pour la connexion d'un utilisateur et l'obtention d'un token JWT
    path('login/', TokenObtainPairView.as_view(), name='login'),
]
