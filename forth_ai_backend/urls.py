"""forth_ai_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
# from django.conf.urls.static import static
# from django.conf import settings
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns

from api import routers

from forth_ai_backend.oauth.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^', include('forth_ai_backend.oauth.urls')),


    # available api
    url(r'^v1/', include(routers.router.urls)),

    
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/github/$', GithubLogin.as_view(), name='github_login'),

    url(r'^user/$', detail, name='detail'),
    url(r'^rest-auth/create/', CreateUser.as_view(), name = 'create_user'),
    url(r'^rest-auth/profiles/', UserList.as_view(), name = 'user_list'),

]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
