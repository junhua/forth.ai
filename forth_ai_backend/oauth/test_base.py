import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.client import Client, MULTIPART_CONTENT
from django.utils.encoding import force_text

from rest_framework import status


class APIClient(Client):

    def patch(self, path, data='', content_type=MULTIPART_CONTENT, follow=False, **extra):
        return self.generic('PATCH', path, data, content_type, **extra)

    def options(self, path, data='', content_type=MULTIPART_CONTENT, follow=False, **extra):
        return self.generic('OPTIONS', path, data, content_type, **extra)


class BaseAPITestCase(object):

    def init(self):
        settings.DEBUG = True
        self.client = APIClient()

        self.register_url = reverse('rest_register')
        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')


    def send_request(self, request_method, *args, **kwargs):
        
        
        if 'content_type' not in kwargs and request_method != 'get':
            kwargs['content_type'] = 'application/json'
        if 'data' in kwargs and request_method != 'get' and kwargs['content_type'] == 'application/json':
            data = kwargs.get('data', '')
            kwargs['data'] = json.dumps(data) 
        
        if hasattr(self, 'token'):
            if getattr(settings, 'REST_USE_JWT', False):
                kwargs['HTTP_AUTHORIZATION'] = 'JWT %s' % self.token
            else:
                kwargs['HTTP_AUTHORIZATION'] = 'Token %s' % self.token

        request_func = getattr(self.client, request_method)
        self.response = request_func(*args, **kwargs)

        is_json = bool(
            [x for x in self.response._headers['content-type'] if 'json' in x])
        self.response.json = {}
        if is_json and self.response.content:
            self.response.json = json.loads(force_text(self.response.content))

        status_code = kwargs.get('status_code')
        if status_code:
            self.assertEqual(self.response.status_code, status_code)

        return self.response

    def post(self, *args, **kwargs):
        return self.send_request('post', *args, **kwargs)
    def get(self, *args, **kwargs):
        return self.send_request('get', *args, **kwargs)
    
    def _login(self):
        data = {
            "email": self.EMAIL,
            "password": self.PASS
        }
        response = self.post(self.login_url, data = data, status_code=status.HTTP_200_OK)

    def _logout(self):
        response = self.post(self.logout_url, status_code=status.HTTP_200_OK)
