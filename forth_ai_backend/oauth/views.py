from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from rest_auth.registration.views import SocialLoginView
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

class CreateUser(SocialLoginView):
	pass


def login_token(provider, access):
	url = 'http://localhost:8000/rest-auth/%s/' % provider
	data = {
		"access_token": access
	}
	response = requests.post(url,data)
	return response.content


def detail(request):
	user = request.user
	url = 'http://localhost:3001'
	provider = str(SocialAccount.objects.filter(user = user)[0].provider)
	access =  str(SocialToken.objects.filter(account__user = user)[0])

	detail = json.loads(login_token(provider, access))

	response = HttpResponseRedirect(url, detail['token'])
	# token is response.content
	return response