from django.urls import path

from .views import UserView, PostView, LoginView, PostListView, FollowView, UnFollowView, LikeView, CommentView, \
    UnLikeView

urlpatterns = [
    path('authenticate/', LoginView.as_view(), name='authenticate'),
    path('user', UserView.as_view(), name='user_view'),
    path('follow/<int:user_id>', FollowView.as_view(), name='follow_view'),
    path('unfollow/<int:user_id>', UnFollowView.as_view(), name='unfollow_view'),
    path('post/', PostView.as_view(), name='create_post'),
    path('post/<int:post_id>', PostView.as_view(), name='get_post'),
    path('post/<int:post_id>/', PostView.as_view(), name='delete_post'),
    path('like/<int:post_id>', LikeView.as_view(), name='like_post'),
    path('unlike/<int:post_id>', UnLikeView.as_view(), name='unlike_post'),
    path('comment/<int:post_id>', CommentView.as_view(), name='comment_post'),
    path('all_posts', PostListView.as_view(), name='all_posts_view'),
]
