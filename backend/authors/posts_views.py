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

# for documentation 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# Main view that checks the request method and delegates to appropriate functions
@api_view(['GET', 'POST'])
def author_posts(request, author_id):
    if request.method == 'GET':
        return list_recent_posts(request, author_id)
    
    elif request.method == 'POST':
        return create_new_post(request, author_id)
    

@swagger_auto_schema(
    method='post',
    operation_summary="Create a new post for a specific author",
    operation_description="""
    **When to use**: Use this endpoint to create a new post for a specific author.

    **How to use**: Send a POST request with the required fields (`title`, `description`, `content`, `contentType`, `visibility`).

    **Why/Why not**: Use this endpoint to allow authors to publish new posts.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'content', 'contentType', 'visibility'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, example="Post Title", description="The title of the post."),
            'description': openapi.Schema(type=openapi.TYPE_STRING, example="A description of the post", description="description to provide context."),
            'contentType': openapi.Schema(type=openapi.TYPE_STRING, example="text/plain", description="The type of content in the post (e.g., plain text, markdown, base64 image)."),
            'content': openapi.Schema(type=openapi.TYPE_STRING, example="This is the content of the post.", description="The main content of the post."),
            'visibility': openapi.Schema(type=openapi.TYPE_STRING, example="PUBLIC", description="Who can see the post (e.g., PUBLIC, UNLISTED, FRIENDS).")
        }
    ),
    responses={
        201: openapi.Response(
            description="Post created successfully",
            examples={
                "application/json": {
                    "id": "550e8400-e29b-41d4-a716-446655440000", 
                    "title": "New Post Title",
                    "description": "A brief description of the post",
                    "contentType": "text/plain",
                    "content": "content of the post!",
                    "author": 3,
                    "visibility": "PUBLIC"
                }
            }
        )
    }
)
# Function to handle post creation (POST)
@api_view(['POST'])
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

@swagger_auto_schema(
    method='get',
    operation_summary="List recent posts by a specific author",
    operation_description="""
    **When to use**: Use this endpoint to retrieve recent posts from a specific author based on visibility and the the user's relationship with the author.

    **How to use**: Send a GET request with the author's ID to retrieve their posts.

    **Why/Why not**: useful to use when you need to view an author's recent posts based on the specfic visbility 
    """,
    responses={
        200: openapi.Response(
            description="A list of recent posts by the author",
            examples={
                "application/json": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Author's Public Post",
                        "description": "Description of the public post",
                        "contentType": "text/plain",
                        "content": "This is the content of the post.",
                        "author": 3,
                        "published": "2023-10-20T14:48:00Z",
                        "visibility": "PUBLIC",
                        "shares_count": 0
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
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
    


@swagger_auto_schema(
    method='put',
    operation_summary="Update an existing post",
    operation_description="""
    **When to use**: Use this endpoint to update an existing post by providing the updated fields.

    **How to use**: Send a PUT request with the updated fields (`title`, `description`, `content`, `contentType`, `visibility`).

    **Why/Why not**: Use this to allow authors to update or edit their posts.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, example="Updated Title", description="Updated title of the post."),
            'description': openapi.Schema(type=openapi.TYPE_STRING, example="Updated description", description="An updated description for the post."),
            'contentType': openapi.Schema(type=openapi.TYPE_STRING, example="text/markdown", description="Updated content type (e.g., text/plain, text/markdown)."),
            'content': openapi.Schema(type=openapi.TYPE_STRING, example="Updated content", description="Updated content of the post."),
            'visibility': openapi.Schema(type=openapi.TYPE_STRING, example="FRIENDS", description="Updated visibility (e.g., PUBLIC, FRIENDS, UNLISTED).")
        }
    ),
    responses={
        200: openapi.Response(
            description="Post updated successfully",
            examples={
                "application/json": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Updated Post Title",
                    "description": "Updated description",
                    "contentType": "text/markdown",
                    "content": "Updated markdown content",
                    "visibility": "FRIENDS",
                    "published": "2023-10-21T10:30:00Z"
                }
            }
        )
    }
)
@api_view(['PUT'])
def update_existing_post(request, author_id, post_id):
    author = get_object_or_404(Author, id=author_id)
    post = get_object_or_404(Post, id=post_id, author=author)
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


@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a post using ID",
    operation_description="""
    **When to use**: Use this endpoint to delete a specific post by its ID.

    **How to use**: Send a DELETE request with the post ID.

    **Why/Why not**: Use this to allow authors to delete posts they have created.
    """,
    responses={
        204: openapi.Response(description="Post deleted successfully"),
        403: openapi.Response(description="Forbidden: You can only delete your own posts")
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

# Delete a post
def delete_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if post.author == request.user:  # Ensure the user is the author of the post
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)  # Forbidden if not the author


@swagger_auto_schema(
    method='get',
    operation_summary="Get all public posts from all authors",
    operation_description="""
    **When to use**: Use this endpoint to get all publicly visible posts from all authors.

    **How to use**: Send a GET request to retrieve all public posts

    **Why/Why not**: Should be used as we would to see streams of only public posts 

    Is not paginated
    """,
    responses={200: openapi.Response(
        description="A list of public posts",
        examples={
            "application/json": {
                "results": [
                    {
                        # example 1
                        "id": "550e8400-e29b-41d4-a716-446655440000",  #unique identifer for post for identification
                        "title": "My First Post",  # title of post 
                        "description": "This is a description for my first post", #description for post 
                        "contentType": "text/plain", # Type of format in this case plain text
                        "content": "content for first page",  # the content of the post 
                        "author": 3, # Id of author who created the post needed for identification
                        "visibility": "PUBLIC",  # indicates who can see the post  
                    },

                    # example 2
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Second Post",
                        "description": "A second example of a public post",
                        "contentType": "text/plain",
                        "content": "Here’s the content for my second post",
                        "author": 4,
                        "visibility": "PUBLIC",
                    }
                ]
            }
        }
    )}
)

@api_view(['GET'])
def get_all_public_posts(request):
    public_posts = Post.objects.filter(visibility="PUBLIC").order_by('-published')
    serialized_posts = [PostSerializer(post).data for post in public_posts]
    return Response({"posts": serialized_posts}, status=200)



@swagger_auto_schema(
    method='post',
    operation_summary="Share a post",
    operation_description="""
    **When to use**: Use this endpoint to share an existing post.

    **How to use**: Send a POST request with the post ID of the post you want to share.

    **Why/Why not**: Use this to allow users to share posts with others, making the shared post visible to a broader audience.
    """,
    responses={
        201: openapi.Response(
            description="Post shared successfully",
            examples={
                "application/json": {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "title": "Shared: Original Post Title",
                    "description": "Description of the original post",
                    "contentType": "text/plain",
                    "content": "Original post content",
                    "author": 5,
                    "published": "2023-10-22T14:00:00Z",
                    "visibility": "PUBLIC",
                    "is_shared": True,
                    "original_post": "550e8400-e29b-41d4-a716-446655440000"
                }
            }
        ),
        403: openapi.Response(description="Forbidden: This post cannot be shared")
    }
)
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

@swagger_auto_schema(
    method='get',
    operation_summary="List all shared posts by an author",
    operation_description="""
    **When to use**: Use this endpoint to retrieve all posts shared by a specific author.

    **How to use**: Send a GET request with the author's ID in the URL. The endpoint returns shared posts that are publicly visible or, if the user is authenticated, may include additional visibility-based posts.

    **Why/Why not**: Use this to see all shared posts from an author, especially if you're following or interested in the author's public content.
    """,
    responses={
        200: openapi.Response(
            description="List of shared posts",
            examples={
                "application/json": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Shared: Original Post Title",
                        "description": "This is a shared post description",
                        "contentType": "text/plain",
                        "content": "This is the content of the shared post",
                        "author": 3,
                        "published": "2023-10-20T14:48:00Z",
                        "visibility": "PUBLIC",
                        "is_shared": True,
                        "original_post": "550e8400-e29b-41d4-a716-446655440001"
                    }
                ]
            }
        ),
        404: openapi.Response(
            description="Author not found",
            examples={
                "application/json": {
                    "detail": "Author not found."
                }
            }
        )
    }
)
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


@swagger_auto_schema(
    method='get',
    operation_summary="Retrieve the stream of relevant posts",
    operation_description="""
    **When to use**: Use this endpoint to retrieve a stream of posts relevant to the authenticated user, based on their follows, friends, and public posts.

    **How to use**: Send a GET request. The endpoint will return public posts and additional posts based on the user's relationships (e.g., followed users, friends).

    **Why/Why not**: Use this to view a personalized feed of posts, filtered based on visibility settings (public, unlisted, friends-only).
    """,
    responses={
        200: openapi.Response(
            description="Stream of posts",
            examples={
                "application/json": {
                    "count": 3,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "title": "Public Post Title",
                            "description": "Description of a public post",
                            "contentType": "text/plain",
                            "content": "This is a public post",
                            "author": 3,
                            "published": "2023-10-20T14:48:00Z",
                            "visibility": "PUBLIC"
                        },
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440001",
                            "title": "Unlisted Post Title",
                            "description": "Description of an unlisted post",
                            "contentType": "text/markdown",
                            "content": "This is an unlisted post",
                            "author": 5,
                            "published": "2023-10-21T10:30:00Z",
                            "visibility": "UNLISTED"
                        },
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440002",
                            "title": "Friends-Only Post Title",
                            "description": "Description of a friends-only post",
                            "contentType": "text/markdown",
                            "content": "This is a friends-only post",
                            "author": 4,
                            "published": "2023-10-21T11:30:00Z",
                            "visibility": "FRIENDS"
                        }
                    ]
                }
            }
        )
    }
)
# Stream for showing all relevant posts
@api_view(['GET'])
def stream(request,author_id):

    # getting all the public posts
    posts = Post.objects.filter(~Q(author=request.user), visibility='PUBLIC')  # public posts excluding the author's own posts
    
    if request.user.is_authenticated:
        # see unlisted posts from people you follow
        following = Follow.objects.filter(follower=request.user, status="FOLLOWED").values_list('user', flat=True)
        following_posts = Post.objects.filter(author__in=following, visibility='UNLISTED')
        
        # see unlisted and friends-only posts from friends
        friends = Follow.get_friends(request.user)
        friends_posts = Post.objects.filter(author__in=friends, visibility__in=['UNLISTED', 'FRIENDS'])

        # see public posts and relevant friends/unlisted posts
        posts = posts | following_posts | friends_posts

    # remove deleted posts
    posts = posts.exclude(is_deleted=True).order_by('-published')

    # paginate the stream
    paginator = PageNumberPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)
