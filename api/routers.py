from rest_framework.routers import DefaultRouter
from apps.posts.views import *

router = DefaultRouter()

# posts
router.register(r'posts', PostViewSet, base_name='posts')
router.register(r'pages', PageViewSet, base_name='pages')
router.register(r'auto', AutoViewSet, base_name='auto')
