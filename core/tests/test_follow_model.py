from django.test import TestCase
from core.models import Follow
from django.contrib.auth.models import User


class TestFollowModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1')
        self.user2 = User.objects.create_user(username='user2', password='user2')

    def test_follow(self):
        follow = Follow.objects.create(follower=self.user1, following=self.user2)
        self.assertEqual(Follow.objects.filter(id=follow.id).exists(), True)
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)
        self.assertEqual(self.user2.followers.filter(follower=self.user1).exists(), True)
        self.assertEqual(self.user1.followings.filter(following=self.user2).exists(), True)

    def test_unfollow(self):
        follow = Follow.objects.create(follower=self.user1, following=self.user2)
        follow.delete()
        self.assertEqual(Follow.objects.filter(id=follow.id).exists(), False)
        self.assertEqual(self.user2.followers.filter(follower=self.user1).exists(), False)
        self.assertEqual(self.user1.followings.filter(following=self.user2).exists(), False)

