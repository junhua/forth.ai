from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection


from rest_framework import (viewsets, 
                            authentication, 
                            permissions, 
                            filters
                            )
from rest_framework import status as status_code
from rest_framework.response import Response


from .models import *
from .serializers import *
from .facebook import *

import requests, json
import time
from allauth.socialaccount.models import SocialToken

from .permissions import IsOwner
from facebook import *


class DefaultsMixin(object):

    """ 
    Default settings for view auth, permissions,
    filtering and pagination
    """

    permission_classes = (
        #permissions.IsAuthenticated,
        #IsOwner,
        permissions.AllowAny,
    )
    paginate_by = 25
    # paginate_by_param = "owner"

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class PostViewSet(DefaultsMixin, viewsets.ModelViewSet):
    # TODO: permission: only page in current user's page can post
    # TODO: filter is changeble

    serializer_class = CreatePostSerializer
    queryset = Post.objects.all()

    def create_page_post(self, pages, post_id):
        for page in pages:
            page_id = page['id']
            print type(page_id)
            data = {
                'page':page_id,
                'post':post_id,
                'is_published':False
            }
            serializer = PagePostSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def create(self, request, *args, **kwargs):

        if 'pages' in request.data:
            pages = request.data.pop('pages')
        else:
            return Response(
                {'detail': 'pages field is required'},
                status=status_code.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.save(owner = owner)
        serializer.save()

        post_id = serializer.data['id']

        self.create_page_post(pages, post_id)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status_code.HTTP_201_CREATED,
            headers=headers
        )

    def list(self, request, *args, **kwargs):
        owner = request.user
        page_id = request.query_params.get('page_id', None)
        status = request.query_params.get('status', None)

        filters = {}
        if page_id:
            if page_id.isdigit():
                page_id = int(page_id)
                page_posts = PagePost.objects.values_list('post', flat=True).filter(page=page_id)
                filters['id__in'] = page_posts
        if status:
            filters['status'] = status

        posts = Post.objects.filter(**filters)
        serializer = CreatePostSerializer(posts, many=True)
        
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UpdatePostSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # refresh the instance from the database.
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        return Response(serializer.data)


    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs) 



        
    # filter_fields = ['owner', ]

    # parser_classes = (MultiPartParser, FormParser,)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super(FileUploaderViewSet, self).get_queryset(*args, **kwargs)
    #     qs = qs.filter(owner=self.request.user)
    #     return qs

class PageViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Pages.objects.all()

    def create(self, request, *args, **kwargs):
        return Response('Method not allowed')
    def update(self, request, *args, **kwargs):
        return Response('Method not allowed')
    def destroy(self, request, *args, **kwargs):
        return Response('Method not allowed')

    def user_access(self, user):
        access =  str(SocialToken.objects.filter(account__user = user)[0])
        return access

    def flush_page(self, user):
        # # facebook page update/create
        # access = self.user_access(user)
        # user_id = self.user_id(user)

        # fb = facebook()
        # pages = fb.get_page(access)['id']
        pass
        
    def user_id(self, user):
        username = user.username
        User = get_user_model()
        user_id = User.objects.get(username=username)
        return user_id

    def list(self, request, *args, **kwargs):
        user = self.request.user
        self.flush_page(user)

        # TODO: get me(api-type=0)/pages(api-type=1) from provider = facebook

        user_id = self.user_id(user)
        user_pages = PageUser.objects.values_list('page', flat=True).filter(user = user_id)
        pages = Pages.objects.filter(id__in=user_pages) #where in
        serializer = self.get_serializer(pages, many=True)
        return Response(serializer.data)



