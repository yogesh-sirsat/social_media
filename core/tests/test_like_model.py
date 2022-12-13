from django.test import TestCase
from core.models import Post, Like
from django.contrib.auth.models import User


class TestLikeModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.user2 = User.objects.create_user(username='user2', password='user2')
        self.user3 = User.objects.create_user(username='user3', password='user3')

        self.post1 = Post.objects.create(author=self.user2, title='title1', description='description1')

    def test_like_create(self):
        like = Like.objects.create(liked_by=self.user1, post=self.post1)
        self.assertEqual(self.post1.likes.filter(id=like.id).exists(), True)
        self.assertEqual(like.liked_by, self.user1)
        self.assertEqual(like.post, self.post1)

    def test_like_delete(self):
        like = Like.objects.create(liked_by=self.user1, post=self.post1)
        like.delete()
        self.assertEqual(Like.objects.filter(id=like.id).exists(), False)

    def test_get_likes_count(self):
        like1 = Like.objects.create(liked_by=self.user1, post=self.post1)
        like2 = Like.objects.create(liked_by=self.user3, post=self.post1)
        self.assertEqual(self.post1.get_likes_count(), 2)
