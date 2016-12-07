from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions, filters
from .models import *
from .serializers import *

import requests
from allauth.socialaccount.models import SocialToken

class DefaultsMixin(object):

    """ 
    Default settings for view auth, permissions,
    filtering and pagination
    """

    permission_classes = (
        permissions.IsAuthenticated,
        #permissions.AllowAny,
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

    def fb_login(self, access, post_data):
        fb_host = 'https://graph.facebook.com/v2.8'
        user_post_api = fb_host + '/me/feed'
        message = post_data.get('content')
        params = {
            'message':message,
            'access_token':access
    
        }
        resp = requests.post(user_post_api, params = params)


    def perform_create(self, serializers):
        # TODO: post to github or fb
        user = self.request.user
        data = self.request.data
        access =  str(SocialToken.objects.filter(account__user = user)[0])
        # POST NLP-->data
        post_data = data # temp
        self.fb_login(access, post_data)

        
    # filter_fields = ['owner', ]

    # parser_classes = (MultiPartParser, FormParser,)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super(FileUploaderViewSet, self).get_queryset(*args, **kwargs)
    #     qs = qs.filter(owner=self.request.user)
    #     return qs
