from rest_framework import generics
from .serializers import UserSerializer

class CreateUserApiView(generics.CreateAPIView):
    """Api view for creating user."""
    serializer_class = UserSerializer

