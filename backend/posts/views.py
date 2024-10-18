from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from .serializers import PostSerializer
from django.contrib.auth import get_user_model
import requests
import json

# Create your views here.
Author = get_user_model()

@api_view(['POST'])
def create_new_post(request,author_id):
    title = request.POST.get('title', '')
    description = request.POST.get('description', '')
    content_type = request.POST.get('contentType', '')
    content = request.POST.get('content', '')

    author = get_object_or_404(Author, id=author_id)

    new_post = Post(title=title, description=description, contentType=content_type, content=content, author=author)
    new_post.save()

    serializer = PostSerializer(new_post)

    return Response(serializer.data, status=201)


@api_view(['PUT'])
def update_existing_post(request, author_id, post_id):
    author = get_object_or_404(Author, id=author_id)
    post = get_object_or_404(Post, id=post_id, author=author)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Get a single post
@api_view(['GET'])
def get_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author_id=author_id)

    # Public and unlisted posts are visible to everyone
    if post.visibility in ['PUBLIC', 'UNLISTED']:
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

    # For friends-only posts, check if the user is authenticated and a friend
    if post.visibility == 'FRIENDS':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required to view this post."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user == post.author or Friend.objects.filter(user=post.author, friend=request.user).exists():
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "This post is only visible to friends."}, status=status.HTTP_403_FORBIDDEN)

    # If we reach here, the post has an invalid visibility setting
    return Response({"detail": "Invalid post visibility setting."}, status=status.HTTP_400_BAD_REQUEST)


# Delete a post
@api_view(['DELETE'])
def delete_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# List recent posts by an author
@api_view(['GET'])
def list_author_posts(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    
    # Get all posts by the author
    posts = Post.objects.filter(author=author).order_by('-published')
    
    # Filter based on visibility and relationship
    if request.user.is_authenticated:
        if request.user == author:
            # Author sees all their own posts
            pass
        elif Friend.objects.filter(user=author, friend=request.user).exists():
            # Friends see public, friends-only, and unlisted posts
            posts = posts.filter(
                Q(visibility='PUBLIC') |
                Q(visibility='FRIENDS') |
                Q(visibility='UNLISTED')
            )
        else:
            posts = posts.filter(visibility='PUBLIC')
    else:
        # Unauthenticated users see only public posts
        posts = posts.filter(visibility='PUBLIC')
    
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_friend(request, author_id):
    friend = get_object_or_404(Author, id=author_id)
    if request.user == friend:
        return Response({"detail": "You can't be friends with yourself."}, status=status.HTTP_400_BAD_REQUEST)
    friendship, created = Friend.objects.get_or_create(user=request.user, friend=friend)
    if created:
        return Response({"detail": "Friend added successfully."}, status=status.HTTP_201_CREATED)
    return Response({"detail": "You are already friends with this user."}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_friend(request, author_id):
    friend = get_object_or_404(Author, id=author_id)
    friendship = Friend.objects.filter(user=request.user, friend=friend).first()
    if friendship:
        friendship.delete()
        return Response({"detail": "Friend removed successfully."}, status=status.HTTP_200_OK)
    return Response({"detail": "You are not friends with this user."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def post_github_activity(request, author_id):
    author = get_object_or_404(User, id=author_id)
    github_username = author.github.split("/")[-1]

    response = requests.get(f"https://api.github.com/users/{github_username}/events")
    events = json.loads(response.content.decode())
    
    for event in events:
        event_type = event['type']
        payload = event['payload']

        new_post = Post()

        if event_type == "IssueEvent":
            pass
        elif event_type == "IssueCommentEvent":
            new_post.title = f"{github_username} commented on an issue in {event['repo']['name']}"
            new_post.description = f"Event Id: {event['id']}"
            new_post.content = f""

    return Response(status=200)
