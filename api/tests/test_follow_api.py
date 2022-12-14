from core.models import Follow
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestFollowApi(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@dummy.com', password='user1')
        self.user2 = User.objects.create_user(username='user2', email='user2@dummy.com', password='user2')

    def test_follow(self):
        message = 'User followed successfully.'
        self.client.post('/api/authenticate/', {'email': 'user1@dummy.com', 'password': 'user1'})
        response = self.client.post(f'/api/follow/{self.user2.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.filter(following=self.user2, follower=self.user1).exists(), True)
        self.assertEqual(self.user2.followers.filter(follower=self.user1).exists(), True)
        self.assertEqual(self.user1.followings.filter(following=self.user2).exists(), True)

    def test_follow_already_following(self):
        message = 'You are already following this user.'
        self.client.post('/api/authenticate/', {'email':  self.user1.email, 'password': 'user1'})
        self.client.post(f'/api/follow/{self.user2.id}')
        response = self.client.post(f'/api/follow/{self.user2.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow(self):
        message = 'User unfollowed successfully.'
        self.client.post('/api/authenticate/', {'email': 'user1@dummy.com', 'password': 'user1'})
        self.client.post(f'/api/follow/{self.user2.id}')
        response = self.client.post(f'/api/unfollow/{self.user2.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.filter(following=self.user2, follower=self.user1).exists(), False)
        self.assertEqual(self.user2.followers.filter(follower=self.user1).exists(), False)
        self.assertEqual(self.user1.followings.filter(following=self.user2).exists(), False)

    def test_unfollow_not_following(self):
        message = 'You are not following this user.'
        self.client.post('/api/authenticate/', {'email':  self.user1.email, 'password': 'user1'})
        response = self.client.post(f'/api/unfollow/{self.user2.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_unauthenticated(self):
        message = 'User is not authenticated.'
        response = self.client.post(f'/api/follow/{self.user2.id}')
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollow_unauthenticated(self):
        message = 'User is not authenticated.'
        response = self.client.post(f'/api/unfollow/{self.user2.id}')
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_invalid_user(self):
        message = 'User does not exists.'
        self.client.post('/api/authenticate/', {'email':  self.user1.email, 'password': 'user1'})
        response = self.client.post(f'/api/follow/999')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_invalid_user(self):
        message = 'User does not exists.'
        self.client.post('/api/authenticate/', {'email':  self.user1.email, 'password': 'user1'})
        response = self.client.post(f'/api/unfollow/999')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_self(self):
        message = 'You cannot follow yourself.'
        self.client.post('/api/authenticate/', {'email':  self.user1.email, 'password': 'user1'})
        response = self.client.post(f'/api/follow/{self.user1.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
