from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

import requests
import json

from forth_ai_backend.oauth import test_base


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



class SocialLoginTests():
	pass




# python manage.py test forth_ai_backend.oauth