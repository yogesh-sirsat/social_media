from django.test import TestCase
from core.models import Post
from django.contrib.auth.models import User


class TestPostModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')

    def test_post_create(self):
        post = Post.objects.create(author=self.user1, title='title1', description='description1')
        self.assertEqual(Post.objects.filter(id=post.id).exists(), True)
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.title, 'title1')
        self.assertEqual(post.description, 'description1')

    def test_post_delete(self):
        post = Post.objects.create(author=self.user1, title='title1', description='description1')
        post.delete()
        self.assertEqual(Post.objects.filter(id=post.id).exists(), False)

