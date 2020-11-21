from .viewsets import MovieViewSet, QuickViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('all', MovieViewSet, basename = 'movie')
router.register('quick', QuickViewSet, basename = 'quick-movie')