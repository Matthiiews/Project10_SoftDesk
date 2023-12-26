from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from api.permissions import UserPermission
from api.serializers.accounts import (
    UserCreateSerializer,
    UserListSerializer,
    UserDetailSerializer
)
from api.views.mixins import SerializerClassMixin

UserModel = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Vue API pour l'inscription de l'utilisateur.
    Cette vue permet aux utilisateurs de s'inscrire en fournissant les
    informations nécessaires.
    """
    serializer_class = UserCreateSerializer


class UserViewSet(SerializerClassMixin, ModelViewSet):
    serializer_class = UserListSerializer
    serializer_create_class = UserCreateSerializer
    serializer_detail_class = UserDetailSerializer
    serializer_list_class = UserListSerializer
    permission_classes = [UserPermission]

    # TODO Permission permettant à l'utilisateur d'accéder uniquement à ses
    # propres données

    def get_queryset(self):
        return UserModel.objects.all().order_by("date_joined")
