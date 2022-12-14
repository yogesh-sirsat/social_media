from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserApi(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@dummy.com', password='user1')

    def test_user_authenticate_fail(self):
        message = 'Please provide both email and password.'
        response = self.client.post('/api/authenticate/', {})  # no data
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/api/authenticate/', {'email': 'user1@dummy.com'})  # no password provided
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/api/authenticate/', {'password': 'user1'})  # no email provided
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        message = 'User does not exists.'
        response = self.client.post('/api/authenticate/',
                                    {'email': 'user1@dummy', 'password': 'user1'})  # invalid email
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        message = 'Incorrect Password.'
        response = self.client.post('/api/authenticate/',
                                    {'email': 'user1@dummy.com', 'password': 'user2'})  # invalid password
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_authenticate_success(self):
        message = 'Authenticated successfully.'
        response = self.client.post('/api/authenticate/', {'email': 'user1@dummy.com', 'password': 'user1'})
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_data_fail(self):
        message = 'User is not authenticated.'
        response = self.client.get('/api/user')
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_data_wrong(self):
        self.client.post('/api/authenticate/', {'email': 'user1@dummy.com', 'password': 'user1'})
        response = self.client.get('/api/user')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['username'], 'user2')
        self.assertNotEqual(response.data['email'], 'user2@dummy.com')
        self.assertNotEqual(response.data['followers'], 1)
        self.assertNotEqual(response.data['followings'], 1)

    def test_get_user_data_success(self):
        self.client.post('/api/authenticate/', {'email': 'user1@dummy.com', 'password': 'user1'})
        response = self.client.get('/api/user')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user1')
        self.assertEqual(response.data['email'], 'user1@dummy.com')
        self.assertEqual(response.data['followers'], 0)
        self.assertEqual(response.data['followings'], 0)
