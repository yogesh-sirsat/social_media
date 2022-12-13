from django.test import TestCase
from core.models import Post, Comment
from django.contrib.auth.models import User


class TestCommentModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.user2 = User.objects.create_user(username='user2', password='user2')
        self.user3 = User.objects.create_user(username='user3', password='user3')

        self.post1 = Post.objects.create(author=self.user2, title='title1', description='description1')

    def test_comment_create(self):
        comment = Comment.objects.create(author=self.user1, post=self.post1, content='content1')
        self.assertEqual(self.post1.comments.filter(id=comment.id).exists(), True)
        self.assertEqual(comment.author, self.user1)
        self.assertEqual(comment.post, self.post1)
        self.assertEqual(comment.content, 'content1')

    def test_get_comments(self):
        comment1 = Comment.objects.create(author=self.user1, post=self.post1, content='content1')
        comment2 = Comment.objects.create(author=self.user3, post=self.post1, content='content2')
        self.assertEqual(self.post1.get_comments_count(), 2)
        self.assertEqual(self.post1.get_comments().filter(id=comment1.id).exists(), True)
        self.assertEqual(self.post1.get_comments().filter(id=comment2.id).exists(), True)

