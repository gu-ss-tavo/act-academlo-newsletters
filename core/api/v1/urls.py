from rest_framework.routers import DefaultRouter

from user.views import RegisterUserViewSet
from newsletter.views import NewsletterViewSet

router = DefaultRouter()

router.register('v1/core/register', RegisterUserViewSet, basename='register')
router.register('v1/newsletters', NewsletterViewSet, basename='newstellers')
