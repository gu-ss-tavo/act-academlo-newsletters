from rest_framework.routers import DefaultRouter

from user.views import RegisterUserViewSet, CustomUserViewSet
from newsletter.views import NewsletterViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

router.register(r'v1/core/user', CustomUserViewSet, basename='user')
router.register(r'v1/core/register', RegisterUserViewSet, basename='register')
router.register(r'v1/newsletters', NewsletterViewSet, basename='newstellers')
