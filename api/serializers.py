from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'id', 'content')
        write_only_fields = ('content',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'description', 'published_at')
        write_only_fields = ('title', 'description')


class PostListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def get_likes(obj):
        return obj.get_likes_count()
