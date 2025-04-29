from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer


class UserRegistration(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
