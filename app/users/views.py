from rest_framework import generics
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, TokenAuthSerializer

class CreateUserApiView(generics.CreateAPIView):
    """Api view for creating user."""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    serializer_class = TokenAuthSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

