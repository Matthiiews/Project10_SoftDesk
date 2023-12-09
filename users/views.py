from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import SignupSerializer


class SignupView(generics.CreateAPIView):
    """API view for user registration.
    This view allows users to register by providing necessary information.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

# Create your views here.
