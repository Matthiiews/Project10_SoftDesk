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
    API view for user registration.
    This view allows users to register by providing necessary information.
    """
    serializer_class = UserCreateSerializer


class UserViewSet(SerializerClassMixin, ModelViewSet):
    serializer_class = UserListSerializer
    serializer_create_class = UserCreateSerializer
    serializer_detail_class = UserDetailSerializer
    serializer_list_class = UserListSerializer
    permission_classes = [UserPermission]

    # TODO permission that just the user can access his own data

    def get_queryset(self):
        return UserModel.objects.all().order_by("date_joined")
