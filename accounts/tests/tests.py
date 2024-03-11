from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Module, UserProfile\

import json

#client side testing
class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userprofile = UserProfile.objects.create(user=self.user, user_type='student', email='test@example.com')

    #testing of userprofile view for both GET and POST
    def test_user_profile_api_get(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('profile_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # #testing the module detail view api 
    def test_module_detail_api(self):
        module = Module.objects.create(title='Test Module', content='Test Content')
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('api_module_detail', args=[module.title]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
#server side testing
class UserProfileAPITest(APITestCase):
    def setUp(self):
        #create a user and profile
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = UserProfile.objects.create(user=self.user, dob='2000-01-01')

    def test_get_user_profile(self):
        self.client.login(username='testuser', password='12345') #simulate login
        url = reverse('profile_api') #URL for the endpoint to test
        response = self.client.get(url) #making a GET request to the endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK) #check if the response status code is 200 (OK)
        self.assertEqual(response.data['dob'], '2000-01-01') #checks if the response data is as expected
