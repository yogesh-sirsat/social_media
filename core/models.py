from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Follow(models.Model):
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    relation_since = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-relation_since',)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', null=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(max_length=250, unique_for_date='published_at', blank=True)
    description = models.TextField(blank=False, null=False)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-published_at', 'title')

    def __str__(self):
        return self.title  # pragma: no cover

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "{}{}{}".format(slugify(self.title), "-", self.id)
            Post.objects.filter(id=self.id).update(slug=self.slug)

    def get_comments(self):
        return self.comments.all()

    def get_comments_count(self):
        return self.comments.count()

    def get_likes_count(self):
        return self.likes.count()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-posted_at',)


class Like(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-liked_at',)

