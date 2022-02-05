from rest_framework import mixins, viewsets

from user.models import CustomUser
from user.serializers import CustomUserSerializer


class RegisterSuperuserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = CustomUserSerializer
    model = CustomUser
