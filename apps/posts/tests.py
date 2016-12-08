
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

from .models import Post


class PostTests(APITestCase):

    def test_create_post_without_auth(self):
        """
        Ensure we can create a new post object.
        """

        url = reverse('posts-list')
        data = {
            "type": 1,
            "themes": ['abc'],
            "keywords": ['def', 'g'],
            "content": "~"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().type, 1)
