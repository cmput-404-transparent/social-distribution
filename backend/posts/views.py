from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from .serializers import PostSerializer
from django.contrib.auth import get_user_model
import requests
import json
from datetime import datetime

from rest_framework.pagination import PageNumberPagination


# Create your views here.
Author = get_user_model()


# Main view that checks the request method and delegates to appropriate functions
@api_view(['GET', 'POST'])
def author_posts(request, author_id):
    if request.method == 'GET':
        return list_recent_posts(request, author_id)
    
    elif request.method == 'POST':
        return create_new_post(request, author_id)



# Function to handle post creation (POST)
@permission_classes([IsAuthenticated])
def create_new_post(request, author_id):
    # Check if the authenticated user matches the author_id
    if str(request.user.id) != str(author_id):
        return Response({
            "detail": "You can only create posts for yourself.",
            "your_id": str(request.user.id),
            "requested_id": author_id
        }, status=status.HTTP_403_FORBIDDEN)

    author = get_object_or_404(Author, id=author_id)

    # Handle both JSON and form data
    if request.content_type == 'application/json':
        data = request.data
    else:
        data = request.POST

    title = data.get('title', '')
    description = data.get('description', '')
    content_type = data.get('contentType', '')
    content = data.get('content', '')
    visibility = data.get('visibility', 'PUBLIC')

    new_post = Post(
        title=title,
        description=description,
        contentType=content_type,
        content=content,
        author=author,
        visibility=visibility
    )
    new_post.save()

    serializer = PostSerializer(new_post)

    return Response(serializer.data, status=status.HTTP_201_CREATED)





# List recent posts by an author
def list_recent_posts(request, author_id):
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

    # Apply pagination
    paginator = PageNumberPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)


    serializer = PostSerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)





# Main view to handle GET, PUT, and DELETE for a specific post
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # Permissions can vary based on the method if needed
def post_detail(request, author_id, post_id):
    # author = get_object_or_404(User, id=author_id)
    # post = get_object_or_404(Post, id=post_id, author=author)

    if request.method == 'GET':
        return get_post(request, author_id, post_id)

    elif request.method == 'PUT':
        return update_existing_post(request, author_id, post_id)

    elif request.method == 'DELETE':
        return delete_post(request, author_id, post_id)
    


def update_existing_post(request, author_id, post_id):
    author = get_object_or_404(Author, id=author_id)
    post = get_object_or_404(Post, id=post_id, author=author)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





# Get a single post
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
def delete_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if post.author == request.user:  # Ensure the user is the author of the post
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)  # Forbidden if not the author





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
    author = Author.objects.get(pk=author_id)
    github_username = author.github.split("/")[-1]

    response = requests.get(f"https://api.github.com/users/{github_username}/events")
    events = json.loads(response.content.decode())
    
    for event in events:
        event_type = event['type']
        payload = event['payload']
        event_id = int(event['id'])

        # if the event was already posted, all subsequent events were also posted
        if Post.objects.filter(github_activity_id=event_id).exists():
            break

        new_post = Post()
        new_post.github_activity_id = event_id
        new_post.contentType = 'text/markdown'
        new_post.author = author

        if event_type == "IssuesEvent":
            issue = payload['issue']
            new_post.title = f"{github_username} {payload['action']} an issue"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f'<b>Issue:</b> "{issue["title"]}"<br>View issue [here]({issue["html_url"]})'
        elif event_type == "IssueCommentEvent":
            issue = payload['issue']
            new_post.title = f"{github_username} commented on an issue"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f'<b>Issue:</b> "{issue["title"]}"<br>View comment [here]({issue["html_url"]})'
        elif event_type == "PullRequestEvent":
            pr = payload['pull_request']
            new_post.title = f"{github_username} {payload['action']} a pull request"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f'<b>Pull Request:</b> "{pr["title"]}"<br>View pull request [here]({pr["html_url"]})'
        elif event_type == "PullRequestReviewCommentEvent":
            comment = payload['comment']
            pr = payload['pull_request']
            new_post.title = f"{github_username} {payload['action']} a comment on a pull request"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f'<b>Pull Request:</b> "{pr["title"]}"<br>View comment [here]({comment["html_url"]})'
        else:
            continue
        
        new_post.save()
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        new_published_date = datetime.strptime(event['created_at'], date_format)

        Post.objects.filter(pk=new_post.pk).update(published=new_published_date)

    return Response(status=200)


@api_view(['GET'])
def get_all_public_posts(request):
    public_posts = Post.objects.filter(visibility="PUBLIC").order_by('-published')
    serialized_posts = [PostSerializer(post).data for post in public_posts]
    return Response({"posts": serialized_posts}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if not post.is_shareable:
        return Response({"detail": "This post cannot be shared."}, status=status.HTTP_403_FORBIDDEN)
    
    share, created = Share.objects.get_or_create(sharer=request.user, post=post)
    
    if created:
        # Create a new post as a share
        shared_post = Post.objects.create(
            author=request.user,
            title=f"Shared: {post.title}",
            content=post.content,
            description=post.description,
            contentType=post.contentType,
            visibility='PUBLIC',  # Ensure shared posts are always public
            is_shared=True,
            original_post=post
        )
        # Increment the shares count of the original post
        post.shares_count += 1
        post.save()
        post.refresh_from_db()
        return Response(PostSerializer(shared_post).data, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "You have already shared this post."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_shared_posts(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    shared_posts = Post.objects.filter(author=author, is_shared=True).order_by('-published')
    
    # Apply visibility filters similar to list_author_posts
    if request.user.is_authenticated:
        if request.user != author:
            shared_posts = shared_posts.filter(visibility='PUBLIC')
    else:
        shared_posts = shared_posts.filter(visibility='PUBLIC')
    
    serializer = PostSerializer(shared_posts, many=True)
    return Response(serializer.data)
