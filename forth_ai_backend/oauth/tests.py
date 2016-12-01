from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.test import APITestCase

import requests
import json

from forth_ai_backend.oauth import test_base


#allauth test
# from allauth.socialaccount.tests import OAuthTestsMixin
from allauth.utils import get_user_model, get_current_site
from allauth.socialaccount.models import (SocialApp, 
										SocialAccount, 
										SocialLogin,
										SocialToken)
from allauth.tests import MockedResponse,mocked_response
from allauth.socialaccount.tests import OAuth2TestsMixin
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

class EmailRegisterTests(TestCase, test_base.BaseAPITestCase):
	PASS = 'thisispass'
	EMAIL = "person1@world.com"
	REGISTRATION_DATA = {
		'email': EMAIL,
		'password1':PASS,
		'password2':PASS
	}


	def setUp(self):
		self.init()


	def test_registration(self):
		user_count = get_user_model().objects.all().count()
		result = self.post(self.register_url, 
			            data = self.REGISTRATION_DATA,
			            status_code = 201)
		new_user = get_user_model().objects.latest('id')
		self.assertEqual(get_user_model().objects.all().count(), user_count + 1)
		self.assertEqual(new_user.email, self.REGISTRATION_DATA['email'])

		self._login()
		self._logout()

	def test_empty_data_registration(self):
		#/rest-auth/registration/
		self.post(self.register_url, data={}, status_code=400)

	def test_login_by_email(self):
		data = {
			"email": "test0@test.com",
			"password" : "thisispass"
		}
		get_user_model().objects.create_user(username = " ",
								email = data["email"],
								password = data["password"]
							    )
		self.post(self.login_url, data=data, status_code=200)
		self.assertIn( 'token', self.response.json.keys() )

	@override_settings(ACCOUNT_LOGOUT_ON_GET=True)
	def test_logout_on_get(self):
		data = {
			"email": "test@test.com",
			"password": "thisispass"
		}
		get_user_model().objects.create_user(username = "test",
								email = data["email"], 
								password = data["password"]
							    )
		self.post(self.login_url, data = data, status_code=200)
		self.get(self.logout_url, status=status.HTTP_200_OK)

	@override_settings(ACCOUNT_LOGOUT_ON_GET=False)
	def test_logout_on_post_only(self):
		data = {
			"email": "test1@test.com",
			"password": "thisispass"
		}
		get_user_model().objects.create_user(username = "test",
								email = data["email"],
								password = data["password"]
							    )
		self.post(self.login_url, data=data, status_code=200)
		self.get(self.logout_url, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


class SocialLoginTests(TestCase, test_base.BaseAPITestCase):
	github_data = """
	{
        "type":"User",
        "organizations_url":"https://api.github.com/users/pennersr/orgs",
        "gists_url":"https://api.github.com/users/pennersr/gists{/gist_id}",
        "received_events_url":"https://api.github.com/users/pennersr/received_events",
        "gravatar_id":"8639768262b8484f6a3380f8db2efa5b",
        "followers":16,
        "blog":"http://www.intenct.info",
        "avatar_url":"https://secure.gravatar.com/avatar/8639768262b8484f6a3380f8db2efa5b?d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png",
        "login":"pennersr",
        "created_at":"2010-02-10T12:50:51Z",
        "company":"IntenCT",
        "subscriptions_url":"https://api.github.com/users/pennersr/subscriptions",
        "public_repos":14,
        "hireable":false,
        "url":"https://api.github.com/users/pennersr",
        "public_gists":0,
        "starred_url":"https://api.github.com/users/pennersr/starred{/owner}{/repo}",
        "html_url":"https://github.com/pennersr",
        "location":"The Netherlands",
        "bio":null,
        "name":"Raymond Penners",
        "repos_url":"https://api.github.com/users/pennersr/repos",
        "followers_url":"https://api.github.com/users/pennersr/followers",
        "id":201022,
        "following":0,
        "email":"raymond.penners@intenct.nl",
        "events_url":"https://api.github.com/users/pennersr/events{/privacy}",
        "following_url":"https://api.github.com/users/pennersr/following"
       }
	"""
	facebook_data = """
        {
           "id": "630595557",
           "name": "Raymond Penners",
           "first_name": "Raymond",
           "last_name": "Penners",
           "email": "raymond.penners@gmail.com",
           "link": "https://www.facebook.com/raymond.penners",
           "username": "raymond.penners",
           "birthday": "07/17/1973",
           "work": [
              {
                 "employer": {
                    "id": "204953799537777",
                    "name": "IntenCT"
                 }
              }
           ],
           "timezone": 1,
           "locale": "nl_NL",
           "verified": true,
           "updated_time": "2012-11-30T20:40:33+0000"
        }"""
    
	def setUp(self):
		settings.DEBUG = True
		self.client = Client()
		self._create_app('github')
		self._create_app('facebook')

		self.init()


	def get_mocked_response(self, data = None):
		if data is None:
			data = self.facebook_data
		return MockedResponse(200, data)

	def _create_app(self, provider):
		app = SocialApp.objects.create(
			provider = provider,
			name = 'test_%s' % provider,
			client_id='app123id_%s' % provider,
			secret='dummy'
		)
		app.sites.add(get_current_site())

	def _login_redirect(self, provider, callback):
		response = self.client.get('/accounts/%s/login/' % provider)
		actual_url = response['location']
		client_id='app123id_%s' % provider
		self.assertEqual(response.status_code, 302)
		self.assertIn(client_id, actual_url)
		self.assertIn(callback, actual_url)

	def get_login_response_json(self, with_refresh_token=True):
		rt = ''
		if with_refresh_token:
			rt = ',"refresh_token": "testrf"'
		return """{
            "uid":"weibo",
            "access_token":"testac"
            %s }""" % rt

	def login(self, provider, resp_mock, process = 'login',with_refresh_token=True):
	    if provider == 'github':
	    	response = self.client.get('/accounts/github/login/',
	    							dict(process = process))
	    else:
	    	response = self.client.get(reverse(provider + '_login'),
                                    dict(process = process))
	    
	    p = urlparse(response['location'])
	    q = parse_qs(p.query)
	    complete_url = reverse(provider + '_callback')
	    self.assertGreater(q['redirect_uri'][0]
                           .find(complete_url), 0)
	    response_json = self.get_login_response_json(
	    	with_refresh_token = with_refresh_token
	    )
	    with mocked_response(
	    	    MockedResponse(200, response_json,{'content-type': 'application/json'}),
	    	    resp_mock
	    	):response = self.client.get(
	    							complete_url,
	    							{'code':'test',
	    							'state': q['state'][0]})
	    return response

	def test_github_login_redirect(self):
		callback = '/oauth/authorize'
		self._login_redirect('github', callback)

	def test_facebook_login_redirect(self):
		callback = '/dialog/oauth'
		self._login_redirect('facebook', callback)

	def test_facebook_getlogin_access(self):
		response = self.get_mocked_response()
		login = self.login('facebook', response)
		socialaccount = SocialAccount.objects.get(uid='630595557')
		self.assertEqual(socialaccount.user.username, 'raymond.penners')
		access =  str(SocialToken.objects.filter(
			account__user = socialaccount.user)[0]
		)
		self.assertEqual(access, 'testac') # get access

	def test_github_getlogin_access(self):
		response = self.get_mocked_response(data = self.github_data)
		login = self.login('github', response)

		socialaccount = SocialAccount.objects.get(uid='201022')
		self.assertEqual(socialaccount.user.username, 'pennersr')
		access =  str(SocialToken.objects.filter(
			account__user = socialaccount.user)[0]
		)
		self.assertEqual(access, 'testac') # get access


# python manage.py test forth_ai_backend
