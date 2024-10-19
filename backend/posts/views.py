from rest_framework.decorators import api_view, permission_classes
from authors.models import *
from .models import *
from rest_framework.response import Response
from authors.serializers import *
from posts.serializers import *
from django.shortcuts import get_object_or_404


@api_view(['GET'])
# Get a single post
def get_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author_id=author_id)

    # Public and unlisted posts are visible to everyone
    if post.visibility in ['PUBLIC', 'UNLISTED']:
        return Response(PostSerializer(post).data, status=200)

    # For friends-only posts, check if the user is authenticated and a friend
    if post.visibility == 'FRIENDS':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required to view this post."}, status=401)
        
        if request.user == post.author or Friend.objects.filter(user=post.author, friend=request.user).exists() or Friend.objects.filter(user=request.user, friend=post.author).exists():
            return Response(PostSerializer(post).data, status=200)
        else:
            return Response({"detail": "This post is only visible to friends."}, status=403)

    # If we reach here, the post has an invalid visibility setting
    return Response({"detail": "Invalid post visibility setting."}, status=400)
