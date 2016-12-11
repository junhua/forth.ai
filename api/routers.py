from rest_framework.routers import DefaultRouter
from apps.posts.views import *

router = DefaultRouter()

# posts
router.register(r'posts', PostViewSet, base_name='posts')
