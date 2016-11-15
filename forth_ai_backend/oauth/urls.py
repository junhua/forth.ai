from django.conf.urls import url 
from .views import facebook_login, github_login

urlpatterns = [
    url(r'rest-auth/facebook/$', facebook_login, name='fb_login'),
    # url(r'rest-auth/github/$', github_login, name='github_login'),
]