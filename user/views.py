from rest_framework import viewsets, mixins, status

from .models import CustomUser
from .serializers import CustomUserSerializer

# Create your views here.
class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = CustomUserSerializer
    model = CustomUser
