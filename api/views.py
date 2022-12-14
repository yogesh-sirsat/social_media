from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Post, Follow, Like
from .serializers import PostSerializer, PostListSerializer, CommentSerializer


def get_jwt_for(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


class LoginView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email is None or password is None:
            return Response({'message': 'Please provide both email and password.'},
                            status=400)
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'message': 'User does not exists.'},
                            status=404)
        if not user.check_password(password):
            return Response({'message': 'Incorrect Password.'},
                            status=401)

        jwt_token = get_jwt_for(user)
        response = Response({'message': 'Authenticated successfully.', 'JWT Tokens': jwt_token})
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=jwt_token['access_token'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        return response


class CustomAuthentication(JWTAuthentication):
    def authenticated_user(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise exceptions.AuthenticationFailed(
                'User is not authenticated.',
                code='no_authorization_header'
            )

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        if user is None:
            raise exceptions.AuthenticationFailed(
                'Unknown user to authenticate.',
                code='user_not_found'
            )
        return user


class UserView(APIView):

    @staticmethod
    def get(request):
        user = CustomAuthentication().authenticated_user(request)

        user_details = {
            'username': user.username,
            'email': user.email,
            'followers': user.followers.count(),
            'followings': user.followings.count(),
        }
        return Response(user_details)


class FollowView(APIView):
    @staticmethod
    def post(request, user_id):
        user = CustomAuthentication().authenticated_user(request)

        follow_user = User.objects.filter(id=user_id).first()
        if follow_user is None:
            return Response({'message': 'User does not exists.'}, status=404)

        follow_relation = follow_user.followers.filter(follower=user).first()
        if follow_relation is not None:
            return Response({'message': 'You are already following this user.'}, status=400)

        if follow_user == user:
            return Response({'message': 'You cannot follow yourself.'}, status=400)

        Follow.objects.create(follower=user, following=follow_user)
        return Response({'message': 'User followed successfully.'})


class UnFollowView(APIView):
    @staticmethod
    def post(request, user_id):
        user = CustomAuthentication().authenticated_user(request)

        following_user = User.objects.filter(id=user_id).first()
        if following_user is None:
            return Response({'message': 'User does not exists.'}, status=404)

        follow_relation = following_user.followers.filter(follower=user).first()
        if follow_relation is None:
            return Response({'message': 'You are not following this user.'}, status=400)

        follow_relation.delete()
        return Response({'message': 'User unfollowed successfully.'})


class PostView(APIView):

    @staticmethod
    def post(request):
        user = CustomAuthentication().authenticated_user(request)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @staticmethod
    def get(request, post_id=None):
        if post_id is not None:
            post = Post.objects.filter(id=post_id).first()
            if post is None:
                return Response({'message': 'Post does not exists.'},
                                status=404)
            serializers = PostSerializer(post)
            data = serializers.data
            data['likes'] = post.get_likes_count()
            data['comments'] = post.get_comments_count()
            return Response(data)

        return Response({'message': 'Please provide post id.'}, status=400)

    @staticmethod
    def delete(request, post_id=None):
        user = CustomAuthentication().authenticated_user(request)

        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({'message': 'Post does not exists.'},
                            status=404)

        if post.author != user:
            return Response({'message': 'You are not authorized to delete this post.'},
                            status=403)

        post.delete()
        return Response({'message': 'Post deleted successfully.'})


class LikeView(APIView):

    @staticmethod
    def post(request, post_id):
        user = CustomAuthentication().authenticated_user(request)

        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({'message': 'Post does not exists.'},
                            status=404)

        if post.likes.filter(liked_by=user.id).exists():
            return Response({'message': 'You have already liked this post.'},
                            status=400)

        Like.objects.create(liked_by=user, post=post)
        return Response({'message': 'You have liked this post.'}, status=201)


class UnLikeView(APIView):

    @staticmethod
    def post(request, post_id):
        user = CustomAuthentication().authenticated_user(request)

        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({'message': 'Post does not exists.'},
                            status=404)

        if not post.likes.filter(liked_by=user.id).exists():
            return Response({'message': 'You have not liked this post.'},
                            status=400)

        post.likes.filter(liked_by=user.id).delete()
        return Response({'message': 'You have unliked this post.'})


class CommentView(APIView):

    @staticmethod
    def post(request, post_id):
        user = CustomAuthentication().authenticated_user(request)

        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return Response({'message': 'Post does not exists.'},
                            status=404)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    authentication_classes = (CustomAuthentication,)

    def get_queryset(self):
        user = CustomAuthentication().authenticated_user(self.request)

        return Post.objects.filter(author=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
