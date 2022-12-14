from core.models import Comment, Post
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestCommentApi(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@dummy.com', password='user1')
        self.user2 = User.objects.create_user(username='user2', email='user2@dummy.com', password='user2')
        self.user3 = User.objects.create_user(username='user3', password='user3')

        self.post1 = Post.objects.create(author=self.user1, title='post1', description='post1')

        # self.client.post('/api/authenticate/', {'email': self.user1.email, 'password': 'user1'})
        #  = self.client.post('/api/post/', {'title': 'Post 1 title', 'description': 'Post 1 description'})

    def test_create_comment_unauthenticated(self):
        message = 'User is not authenticated.'
        response = self.client.post(f'/api/comment/{self.post1.id}', {'content': 'comment1'})
        self.assertEqual(response.data['detail'], message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment(self):
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        response = self.client.post(f'/api/comment/{self.post1.id}', {'content': 'comment1'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(id=response.data['id']).exists(), True)
        self.assertEqual(response.data['author'], self.user2.id)
        self.assertEqual(response.data['content'], 'comment1')

    def test_create_comment_invalid_post(self):
        message = 'Post does not exists.'
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        response = self.client.post(f'/api/comment/999', {'content': 'comment1'})
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment_invalid_content(self):
        self.client.post('/api/authenticate/', {'email': self.user2.email, 'password': 'user2'})
        response = self.client.post(f'/api/comment/{self.post1.id}', {'content': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



