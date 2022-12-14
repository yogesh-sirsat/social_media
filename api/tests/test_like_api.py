from core.models import Like, Post
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestLikeApi(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@dummy.com', password='user1')
        self.user2 = User.objects.create_user(username='user2', email='user2@dummy.com', password='user2')

        self.post1 = Post.objects.create(author=self.user1, title='post1', description='post1')

    def test_create_like_unauthenticated(self):
        message = 'User is not authenticated.'
        response = self.client.post(f'/api/like/{self.post1.id}')
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_like(self):
        message = 'You have liked this post.'
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        response = self.client.post(f'/api/like/{self.post1.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post1.likes.filter(liked_by=self.user2).exists(), True)

    def test_create_like_invalid_post(self):
        message = 'Post does not exists.'
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        response = self.client.post(f'/api/like/999')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_like_duplicate(self):
        message = 'You have already liked this post.'
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        self.client.post(f'/api/like/{self.post1.id}')
        response = self.client.post(f'/api/like/{self.post1.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_like_unauthenticated(self):
        message = 'User is not authenticated.'
        response = self.client.post(f'/api/unlike/{self.post1.id}')
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_like(self):
        message = 'You have unliked this post.'
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        self.client.post(f'/api/like/{self.post1.id}')
        response = self.client.post(f'/api/unlike/{self.post1.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post1.likes.filter(liked_by=self.user2).exists(), False)

    def test_delete_like_invalid_post(self):
        message = 'Post does not exists.'
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        response = self.client.post(f'/api/unlike/999')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_like_not_liked(self):
        message = 'You have not liked this post.'
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        response = self.client.post(f'/api/unlike/{self.post1.id}')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
