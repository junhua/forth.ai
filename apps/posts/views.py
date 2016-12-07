from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions, filters
from .models import *
from .serializers import *


class DefaultsMixin(object):

    """ 
    Default settings for view auth, permissions,
    filtering and pagination
    """
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        # permissions.IsAuthenticated,
        permissions.AllowAny,
    )
    paginate_by = 25
    # paginate_by_param = "owner"

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class RepostViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = RepostSerializer
    queryset = Post.objects.all()
    # filter_fields = ['owner', ]

    # parser_classes = (MultiPartParser, FormParser,)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super(FileUploaderViewSet, self).get_queryset(*args, **kwargs)
    #     qs = qs.filter(owner=self.request.user)
    #     return qs
