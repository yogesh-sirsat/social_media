from django.contrib import admin
from .models import Post, Comment, Like, Follow
from django.contrib.auth.models import User


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'get_comments_count', 'get_likes_count')
    list_filter = ('published_at', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('-published_at', 'title')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'posted_at')
    list_filter = ('posted_at', 'author')
    search_fields = ('content',)
    raw_id_fields = ('author', 'post')
    date_hierarchy = 'posted_at'
    ordering = ('-posted_at',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('liked_by', 'post', 'liked_at')
    list_filter = ('liked_at', 'liked_by')
    raw_id_fields = ('liked_by', 'post')
    date_hierarchy = 'liked_at'
    ordering = ('-liked_at',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'relation_since')
    list_filter = ('relation_since', 'follower', 'following')
    raw_id_fields = ('follower', 'following')
    date_hierarchy = 'relation_since'
    ordering = ('-relation_since',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
