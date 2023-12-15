from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from projects.permissions import UserPermission
from projects.serializers.accounts import (
    UserCreationSerializer
)


class SignupView(generics.CreateAPIView):
    """
    API view for user registration.
    This view allows users to register by providing necessary information.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

# Create your views here.
