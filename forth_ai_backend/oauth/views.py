from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialToken, SocialAccount
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:3001'

class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:3001'

def detail(request):
	user = request.user
	provider = str(SocialAccount.objects.filter(user = user)[0].provider)
	access =  str(SocialToken.objects.filter(account__user = user)[0])

	if provider == 'facebook':
		url = 'http://localhost:3001/facebook/login?access=%s & provider=%s'%(access, provider)
	elif provider == 'github':
		url = 'http://localhost:3001/github/login?access=%s & provider=%s'%(access, provider)

	response = HttpResponseRedirect(url)
	response.set_cookie('provider', provider)
	response.set_cookie('access', access)
	response['provider'] = provider
	response['access'] = access

	return response