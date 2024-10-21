from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from posts.serializers import *
from posts.models import *
from posts.views import get_post
from rest_framework.pagination import PageNumberPagination

import base64
from django.http import HttpResponse, JsonResponse

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
    new_post.fqid = new_post.id
    new_post.save()

    serializer = PostSerializer(new_post)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


# List recent posts by an author
def list_recent_posts(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    
    # Get all posts by the author
    posts = Post.objects.filter(author=author,is_deleted=False).order_by('-published')
    
    # Filter based on visibility and relationship
    if request.user.is_authenticated:
        if request.user == author:
            # Author sees all their own posts
            pass
        elif Follow.are_friends(author, request.user):
            # Friends see public, friends-only, and unlisted posts
            posts = posts.filter(
                Q(visibility='PUBLIC') |
                Q(visibility='FRIENDS') |
                Q(visibility='UNLISTED')
            )
        elif Follow.are_friends(author, request.user):
            # followers can see public and unlisted posts
            posts = posts.filter(
                Q(visibility='PUBLIC') |
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

    serializer = PostSummarySerializer(paginated_posts, many=True)

    response_data = {
        "type": "posts",
        "posts": serializer.data
    }

    return Response(response_data, status=200)


# Main view to handle GET, PUT, and DELETE for a specific post
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, author_id, post_id):
    # author = get_object_or_404(User, id=author_id)
    post = get_object_or_404(Post, id=post_id, author_id=author_id)

    if request.method == 'GET':
        if post.visibility in ['PUBLIC', 'UNLISTED']:
            return Response(PostSummarySerializer(post).data, status=200)

        if post.visibility == 'FRIENDS':
            if request.user.is_authenticated:
                return Response(PostSummarySerializer(post).data, status=200)
            else:
                return Response({"detail": "Must be authenticated to view friends only posts."}, status=401)

        return Response({"detail": "Invalid post visibility setting."}, status=400)

    elif request.method == 'PUT':
        if request.user.is_authenticated:
            return update_existing_post(request, author_id, post_id)
        return Response({"detail": "Must be authenticated to update posts."}, status=401) 

    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            return delete_post(request, author_id, post_id)
        return Response({"detail": "Must be authenticated to delete posts."}, status=401)
    

def update_existing_post(request, author_id, post_id):
    author = get_object_or_404(Author, id=author_id)
    post = get_object_or_404(Post, id=post_id, author=author)

    if request.user != author:
        return Response({"detail": "You don't have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
    data = request.data

     # For example, updating specific fields
    post.title = data.get('title', post.title)
    post.description = data.get('description', post.description)
    post.content = data.get('content', post.content)
    post.contentType = data.get('contentType', post.contentType)
    post.visibility = data.get('visibility', post.visibility)

    post.save()


    response_data = {
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'content': post.content,
        'contentType': post.contentType,
        'visibility': post.visibility,
        'published': post.published,
    } 

    return Response(response_data, status=status.HTTP_200_OK)
 

# Delete a post
def delete_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if post.author == request.user:  # Ensure the user is the author of the post
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)  # Forbidden if not the author


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


# Stream for showing all relevant posts
@api_view(['GET'])
def stream(request,author_id):

    author = Author.objects.get(id=author_id)

    # getting all the public posts
    posts = Post.objects.filter(~Q(author=author), visibility='PUBLIC')  # public posts excluding the author's own posts
    
    if author.is_authenticated:
        # see unlisted posts from people you follow
        following = Follow.objects.filter(follower=author, status="FOLLOWED").values_list('user', flat=True)
        following_posts = Post.objects.filter(author__in=following, visibility='UNLISTED')
        
        # see unlisted and friends-only posts from friends
        friends = Follow.get_friends(author)
        friends_posts = Post.objects.filter(author__in=friends, visibility__in=['UNLISTED', 'FRIENDS'])

        # see public posts and relevant friends/unlisted posts
        posts = posts | following_posts | friends_posts

    # remove deleted posts
    posts = posts.exclude(is_deleted=True).order_by('-published')

    # paginate the stream
    paginator = PageNumberPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)

    serializer = PostSummarySerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_image_post(request, author_id, post_id):
    # Get the post by author_serial and post_serial
    post = get_object_or_404(Post, id=post_id, author_id=author_id)

    # Check if the contentType is an image
    if not post.contentType.startswith('image/'):
        return JsonResponse({"detail": "Not an image post"}, status=404)

    # Decode the base64 content to binary
    try:
        image_data = base64.b64decode(post.content)
    except base64.binascii.Error:
        return JsonResponse({"detail": "Invalid image data"}, status=400)

    # Return the image as a binary
    return HttpResponse(image_data, content_type=post.contentType)