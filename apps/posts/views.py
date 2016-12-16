from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection
from django.http import HttpResponseForbidden

from rest_framework import (viewsets, 
                            authentication, 
                            permissions, 
                            filters
                            )
from rest_framework import status as status_code
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from .models import *
from .serializers import *
from .facebook import Facebook

import requests, json
import time
from allauth.socialaccount.models import SocialToken

from .permissions import IsOwner
import datetime

class DefaultsMixin(object):

    """ 
    Default settings for view auth, permissions,
    filtering and pagination
    """

    permission_classes = (
        permissions.IsAuthenticated,
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

def get_user_access(user):
    access =  str(SocialToken.objects.filter(account__user = user)[0])
    return access

def get_user_id(user):
    username = user.username
    User = get_user_model()
    user_id = User.objects.get(username=username).id
    return user_id

def social_post(post_ids):
    time_format = '%Y-%m-%dT%H:%M:%SZ'
    time_current = time.strftime(time_format)

    for post_id in post_ids:
        print 'tho', post_id
 
        post = Post.objects.filter(id = post_id)
        print 'get post is------???', post

        post_obj = post[0]
        user_obj = post_obj.owner

        access = get_user_access(user_obj)
        content = post_obj.content
        page_obj = post_obj.page

        if page_obj.provider == 'facebook':
            print 'post to facebook'
            fb = Facebook()
            if page_obj.type == 0:
                print 'post to me'
                response = fb.user_post(access, content)
                if response.status_code == status_code.HTTP_200_OK:
                    post.update(status = 1, 
                        publish_date = time_current)
            else:
                print 'post to page', page_obj.uid
                response = fb.page_post(page_obj.uid, access, content)
                if response.status_code == status_code.HTTP_200_OK:
                    post.update(status = 1, 
                        publish_date = time_current)

        elif page_obj.provider == 'google':
            pass
        else:
            pass

def dealwith_content(content):
    # TODO: dedalwith content
    return content

class PostViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = CreatePostSerializer
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        owner = request.user

        if 'pages' in request.data:
            pages = request.data['pages']
        else:
            return Response(
                {'detail': 'pages field is required'},
                status=status_code.HTTP_400_BAD_REQUEST
            )

        is_published = False
        if 'publish_now' in request.data:
            publish_now = request.data['publish_now']# True  
        else:
            return Response(
                {'detail': 'publish_now field is required'},
                status=status_code.HTTP_400_BAD_REQUEST
            )

        response = {}
        response['posts'] = []
        post_ids = []
        for page in pages:
            page_id = page['id']
            try:
                page = Pages.objects.get(id = page_id)
            except Pages.DoesNotExist:
                return  Response(
                {'detail': 'page id is not exist'},
                status=status_code.HTTP_400_BAD_REQUEST
            )
            
            if PageUser.objects.filter(user=owner, page=page_id).exists():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(owner = owner, page = page)

                if not publish_now:
                    response['posts'].append(serializer.data)
                
                post_ids.append(serializer.data['id'])

        if publish_now:
            social_post(post_ids)
            posts = Post.objects.filter(id__in=post_ids)
            serializer = self.get_serializer(posts, many=True)
            response['posts'] = serializer.data

        return Response(
            response,
            status=status_code.HTTP_201_CREATED
        )

    @detail_route(methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def existed_post(self, request, pk=None):
        user = request.user

        publish_now = request.data.get('publish_now', None)

        if publish_now:
            user = self.request.user
            try:
                post = Post.objects.get(id=pk)

                if not PageUser.objects.filter(user=user, page=post.page).exists():
                    return Response(
                        {'detail': 'page does not belong to user'},
                        status=status_code.HTTP_403_FORBIDDEN
                    )

                social_post([pk])
                post = Post.objects.get(id=pk)
            except post.DoesNotExist:
                return Response(
                {'detail': 'Post not exist, check your id'},
                status=status_code.HTTP_400_BAD_REQUEST
            )
            
            serializer = ShowPostSerializer(post)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status_code.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                {'detail': 'publish_now'},
                status=status_code.HTTP_400_BAD_REQUEST
            )


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ShowPostSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        user = request.user

        page_id = request.query_params.get('page', None)
        status = request.query_params.get('status', None)

        filters = {}

        if page_id and page_id.isdigit():
            page_id = int(page_id)
            filters['page'] = page_id

            if not PageUser.objects.filter(user=user, page=page_id).exists():
                return Response(
                    {'detail': 'page does not belong to user'},
                    status=status_code.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'detail': 'page id is required'},
                status=status_code.HTTP_400_BAD_REQUEST
            )

        if status:
            filters['status'] = status

        posts = Post.objects.filter(**filters)
        serializer = ShowPostSerializer(posts, many=True)
        
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user

        instance = self.get_object()

        if not PageUser.objects.filter(user=user, page=instance.page).exists():
            return Response(
                {'detail': 'page does not belong to user'},
                status=status_code.HTTP_403_FORBIDDEN
            )

        partial = kwargs.pop('partial', False)
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



def task():
    from django.utils import timezone
    time_current = timezone.now()
    last_post = time_current - datetime.timedelta(minutes = 1)

    posts = Post.objects.filter( publish_date__range = (last_post, time_current) )
    if posts.exists():
        post_ids = posts.objects.values_list('id', flat=True).filter(status=0)
        if post_ids:
            social_post(post_ids)


class PageViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Pages.objects.all()

    def create(self, request, *args, **kwargs):
        return Response('Method not allowed')
    def update(self, request, *args, **kwargs):
        return Response('Method not allowed')
    def destroy(self, request, *args, **kwargs):
        return Response('Method not allowed')

    def flush_page(self, user): # get facebook datas
        # facebook page update/create
        access = get_user_access(user)
        fb = Facebook()
        pages = []
        account = fb.get_me(access)
        pages.append(account)

        if fb.get_pages(access):
            pages += fb.get_pages(access)

        for page in pages:
            qs = Pages.objects.filter(uid=page['uid'])
            if qs.exists():
                qs.update(**page)
            else:
                Pages.objects.create(**page)

            page_instance = Pages.objects.filter(uid=page['uid'])[0]
            page_id = page_instance.id

            if not PageUser.objects.filter(user=user.id, page=page_id).exists():
                PageUser.objects.create(user=user, page=page_instance)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        self.flush_page(user)

        user_id = get_user_id(user)
        user_pages = PageUser.objects.values_list('page', flat=True).filter(user = user_id)
        pages = Pages.objects.filter(id__in=user_pages) #where in
        serializer = self.get_serializer(pages, many=True)
        return Response(serializer.data)