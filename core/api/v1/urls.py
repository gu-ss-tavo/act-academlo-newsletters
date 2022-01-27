from rest_framework.routers import DefaultRouter

from user.views import RegisterUserViewSet

router = DefaultRouter()

router.register('v1/core/register', RegisterUserViewSet, basename='register')
