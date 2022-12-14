from core.models import Post
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestPostApi(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@dummy.com', password='user1')
        self.user2 = User.objects.create_user(username='user2', email='user2@dummy.com', password='user2')

    def test_create_post_unauthenticated(self):
        message = 'User is not authenticated.'
        response = self.client.post('/api/post/', {'title': 'title1', 'description': 'description1'})
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post(self):
        self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        response = self.client.post('/api/post/', {'title': 'title1', 'description': 'description1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.filter(id=response.data['id']).exists(), True)
        self.assertEqual(response.data['author'], self.user1.id)
        self.assertEqual(response.data['title'], 'title1')
        self.assertEqual(response.data['description'], 'description1')

    def test_create_post_fail(self):
        self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        message = 'This field is required.'
        response = self.client.post('/api/post/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_post_by_id(self):
        self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        response = self.client.post('/api/post/', {'title': 'title1', 'description': 'description1'})
        post_id = response.data['id']
        response = self.client.get(f'/api/post/{post_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], post_id)
        self.assertEqual(response.data['author'], self.user1.id)
        self.assertEqual(response.data['title'], 'title1')
        self.assertEqual(response.data['description'], 'description1')
        self.assertEqual(response.data['likes'], 0)
        self.assertEqual(response.data['comments'], 0)

    def test_get_post_by_id_fail(self):
        message = 'Post does not exists.'
        response = self.client.get('/api/post/1/')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        message = 'Please provide post id.'
        response = self.client.get('/api/post/')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_posts_by_authenticated_user(self):
        self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        response = self.client.post('/api/post/', {'title': 'title1', 'description': 'description1'})
        post1_id = response.data['id']
        response = self.client.post('/api/post/', {'title': 'title2', 'description': 'description2'})
        post2_id = response.data['id']
        response = self.client.get('/api/all_posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['author'], self.user1.id)
        self.assertEqual(response.data[1]['author'], self.user1.id)

    def test_get_all_posts_by_unauthenticated_user(self):
        message = 'User is not authenticated.'
        response = self.client.get('/api/all_posts')
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_by_unauthenticated_user(self):
        message = 'User is not authenticated.'
        response = self.client.delete('/api/post/1/')
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_by_authenticated_user(self):
        message = 'Post deleted successfully.'
        self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        response = self.client.post('/api/post/', {'title': 'title1', 'description': 'description1'})
        post1_id = response.data['id']
        response = self.client.delete(f'/api/post/{post1_id}/')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.filter(id=post1_id).exists(), False)

    def test_delete_post_by_authenticated_user_fail(self):
        self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        message = 'Post does not exists.'
        response = self.client.delete('/api/post/1/')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_by_non_author(self):
        self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        response = self.client.post('/api/post/', {'title': 'title1', 'description': 'description1'})
        post1_id = response.data['id']

        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        message = 'You are not authorized to delete this post.'
        response = self.client.delete(f'/api/post/{post1_id}/')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

