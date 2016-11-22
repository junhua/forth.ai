from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.permissions import IsAdminUser
from rest_framework import generics, mixins

from rest_auth.registration.views import SocialLoginView, RegisterView
from rest_auth.serializers import *
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialToken, SocialAccount

import requests, json

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:3001'

class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:3001'

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserDetailsSerializer
	permission_classes = (IsAdminUser, )

class CreateUser(RegisterView):
	permission_classes = (IsAdminUser, )


def login_token(provider, access):
	url = 'http://localhost:8000/rest-auth/%s/' % provider
	data = {
		"access_token": access
	}
	response = requests.post(url,data)
	return response.content


def detail(request):
	user = request.user
	provider = str(SocialAccount.objects.filter(user = user)[0].provider)
	access =  str(SocialToken.objects.filter(account__user = user)[0])

	detail = json.loads(login_token(provider, access))
	jwt = detail['token']
	url = 'http://www.baidu.com?jwt=%s'%jwt
	response = HttpResponseRedirect(url, jwt)
	response.set_cookie('jwt', value = jwt, domain = '.uiplay.cn')

	return response