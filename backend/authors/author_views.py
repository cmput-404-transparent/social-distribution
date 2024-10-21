from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import *
from .serializers import AuthorSerializer
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_side_login
from rest_framework.authtoken.models import Token
from django.db.models import Q


# for documentation 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    operation_summary="User login",
    operation_description="""
    **When to use**: Use this endpoint to log in a user using their username and password.

    **How to use**: Send a POST request with the `username` and `password`.

    **Why/Why not**: Use this endpoint to authenticate a user and retrieve their authentication token.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, example="user123", description="The username of the user."),
            'password': openapi.Schema(type=openapi.TYPE_STRING, example="password123", description="The password of the user.")
        }
    ),
    responses={
        200: openapi.Response(
            description="User logged in successfully",
            examples={
                "application/json": {
                    "token": "somerandomauthtoken",
                    "userId": 1
                }
            }
        ),
        401: openapi.Response(
            description="Invalid credentials",
            examples={
                "application/json": {
                    "detail": "Invalid credentials"
                }
            }
        )
    }
)
@api_view(['POST'])
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_side_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "userId": user.id}, status=200)
    else:
        return Response(status=401)

@swagger_auto_schema(
    method='post',
    operation_summary="User signup",
    operation_description="""
    **When to use**: Use this endpoint to create a new user account

    **How to use**: Send a POST request with the required details (`username`, `password`, `displayName`, and `github`).

    **Why/Why not**: Use this endpoint to create a new author and log in the user
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, example="johndoe", description="The username for the new account."), 
            'password': openapi.Schema(type=openapi.TYPE_STRING, example="password123", description="The password for the new account."),
            'displayName': openapi.Schema(type=openapi.TYPE_STRING, example="John Doe", description="The display name for the new account."),
            'github': openapi.Schema(type=openapi.TYPE_STRING, example="johndoe", description="The GitHub username for the new account.")
        }
    ),
    responses={
        200: openapi.Response(
            description="User signed up successfully",
            examples={
                "application/json": {
                    "token": "someauthtoken",
                    "userId": 1
                }
            }
        ),
        400: openapi.Response(
            description="Invalid signup details",
            examples={
                "application/json": {
                    "errors": ["Username is taken", "Invalid GitHub username"]
                }
            }
        )
    }
)

@api_view(['POST'])
def signup(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    display_name = request.POST.get('displayName', '')
    github_username = request.POST.get('github', '')
    github_link = f"http://github.com/{github_username}"
    host = request.POST.get('origin', '') + '/api/'

    if not display_name:
        display_name = username

    new_author = Author(username=username, host=host, display_name=display_name, github=github_link)
    new_author.set_password(password)
    new_author.save()
    
    page = f"{request.POST.get('origin', '')}/authors/{new_author.id}"
    new_author.page = page
    new_author.save()

    user = authenticate(request, username=username, password=password)
    django_side_login(request, user)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key, "userId": user.id}, status=200)

@swagger_auto_schema(
    method='get',
    operation_summary="Get author details by ID",
    operation_description="""
    **When to use**: Use this endpoint to retrieve the details of an author by their ID.

    **How to use**: Send a GET request with the author's ID in the URL.

    **Why/Why not**: Use this to get information about an author.
    """,
    responses={
        200: openapi.Response(
            description="Author details",
            examples={
                "application/json": {
                    "id": 1,
                    "username": "johndoe",
                    "display_name": "John Doe",
                    "github": "http://github.com/johndoe",
                    "page": "/authors/1"
                }
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
def get_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    serializer = AuthorSerializer(author, request_user=author)
    return Response(serializer.data, status=200)

@swagger_auto_schema(
    method='get',
    operation_summary="Get author from session token",
    operation_description="""
    **When to use**: Use this endpoint to retrieve the author's ID using a session token.

    **How to use**: Send a GET request with the session token.

    **Why/Why not**: Use this to get the author's ID from the session.
    """,
    responses={
        200: openapi.Response(
            description="Author ID",
            examples={
                "application/json": {
                    "userId": 1
                }
            }
        ),
        400: openapi.Response(
            description="Invalid session token",
            examples={
                "application/json": {
                    "detail": "Invalid session token."
                }
            }
        )
    }
)
@api_view(['GET'])
def get_author_from_session(request):
    session_token = request.GET.get('session')
    token_obj = Token.objects.get(key=session_token)
    return Response({'userId': token_obj.user_id}, status=200)


@swagger_auto_schema(
    method='post',
    operation_summary="Edit author details",
    operation_description="""
    **When to use**: Use this endpoint to update an author's details.

    **How to use**: Send a POST request with the updated author details.

    **Why/Why not**: Use this to modify your own author details.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, example="johndoe", description="The updated username."),
            'password': openapi.Schema(type=openapi.TYPE_STRING, example="newpassword", description="The updated password."),
            'displayName': openapi.Schema(type=openapi.TYPE_STRING, example="John Doe", description="The updated display name."),
            'github': openapi.Schema(type=openapi.TYPE_STRING, example="johndoe", description="The updated GitHub username.")
        }
    ),
    responses={
        200: openapi.Response(
            description="Author updated successfully"
        ),
        400: openapi.Response(
            description="Invalid update details",
            examples={
                "application/json": {
                    "errors": ["Username is taken"]
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized to modify other user's details",
            examples={
                "application/json": {
                    "error": "Cannot modify other user's details!"
                }
            }
        )
    }
)

@api_view(['POST'])
def edit_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    if request.user != author:
        return Response({"error": "Cannot modify other user's posts!"}, status=401)

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    display_name = request.POST.get('displayName', None)
    github = request.POST.get('github', None)

    errors = []

    if username is not None and username != author.username:
        original_username = author.username
        try:
            author.username = username
            author.save()
        except:
            author.username = original_username
            errors.append("Username is taken")
    if password is not None and password and not author.check_password(password):     # checks if passwords are the same
        author.set_password(password)           # if not then change it
    if display_name is not None and display_name != author.display_name:
        author.display_name = display_name
    if github is not None and github != author.github:
        author.github = github
    
    author.save()

    if errors:
        return Response({'errors': errors}, status=400)
    else:
        return Response(status=200)

@swagger_auto_schema(
    method='get',
    operation_summary="Search authors by keyword",
    operation_description="""
    **When to use**: Use this endpoint to search for authors by keyword.

    **How to use**: Send a GET request with the search keyword.

    **Why/Why not**: Use this to find authors by username or display name.
    """,
    responses={
        200: openapi.Response(
            description="Search results",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "username": "johndoe",
                        "display_name": "John Doe",
                        "github": "http://github.com/johndoe",
                        "page": "/authors/1"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def search_author(request):
    keyword = request.GET.get("keyword", '')

    keyword = keyword.split("=")[1] if keyword else keyword

    results = []
    if keyword:
        results = Author.objects.filter(Q(username__icontains=keyword) | Q(display_name__icontains=keyword))
    
    results = [AuthorSerializer(author).data for author in results]

    return Response(results, status=200)


@swagger_auto_schema(
    method='post',
    operation_summary="Follow an author",
    operation_description="""
    **When to use**: Use this endpoint to follow an author.

    **How to use**: Send a POST request with the `user` ID and `follower` ID.

    **Why/Why not**: Use this to follow another author.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user', 'follower'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="The ID of the author to follow."),
            'follower': openapi.Schema(type=openapi.TYPE_INTEGER, example=2, description="The ID of the author who is following.")
        }
    ),
    responses={
        201: openapi.Response(
            description="Follow request created"
        ),
        400: openapi.Response(
            description="Invalid follow request",
            examples={
                "application/json": {
                    "message": "user and/or follower does not exist"
                }
            }
        )
    }
)
@api_view(['POST'])
def follow(request):
    user = request.POST.get('user', None)
    follower = request.POST.get('follower', None)

    if user and follower:
        user_author = Author.objects.get(id=user)
        follower_author = Author.objects.get(id=follower)

        Follow.objects.get_or_create(user=user_author, follower=follower_author)

        return Response(status=201)

    else:
        return Response("user and/or follower does not exist", status=400)
    

@swagger_auto_schema(
    method='get',
    operation_summary="Get follow requests",
    operation_description="""
    **When to use**: Use this endpoint to retrieve pending follow requests for an author.

    **How to use**: Send a GET request with the author's ID.

    **Why/Why not**: Use this to get all pending follow requests for an author.
    """,
    responses={
        200: openapi.Response(
            description="List of follow requests",
            examples={
                "application/json": [
                    {
                        "id": 2,
                        "username": "janedoe",
                        "display_name": "Jane Doe",
                        "github": "http://github.com/janedoe",
                        "page": "/authors/2"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def get_follow_requests(request, author_id):
    author = Author.objects.get(id=author_id)
    follow_requests = Follow.objects.filter(user=author, status="REQUESTED").values_list('follower')
    follow_requests_authors = Author.objects.filter(id__in=follow_requests)
    serialized_follow_requests = [AuthorSerializer(request).data for request in follow_requests_authors]
    return Response(serialized_follow_requests, status=200)


@swagger_auto_schema(
    method='put',
    operation_summary="Accept follow request",
    operation_description="""
    **When to use**: Use this endpoint to accept a follow request.

    **How to use**: Send a PUT request with the author's ID and the follower's ID.

    **Why/Why not**: Use this to accept follow requests for an author.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['follower'],
        properties={
            'follower': openapi.Schema(type=openapi.TYPE_INTEGER, example=2, description="The ID of the follower.")
        }
    ),
    responses={
        200: openapi.Response(
            description="Follow request accepted"
        ),
        400: openapi.Response(
            description="Invalid follow request",
            examples={
                "application/json": {
                    "message": "author and/or follower doesn't exist"
                }
            }
        )
    }
)
@swagger_auto_schema(
    method='delete',
    operation_summary="Delete follow request",
    operation_description="""
    **When to use**: Use this endpoint to delete a follow request.

    **How to use**: Send a DELETE request with the author's ID and the follower's ID.

    **Why/Why not**: Use this to remove a follow request.
    """,
    responses={
        200: openapi.Response(
            description="Follow request deleted"
        ),
        400: openapi.Response(
            description="Invalid follow request",
            examples={
                "application/json": {
                    "message": "author and/or follower doesn't exist"
                }
            }
        )
    }
)
@api_view(["PUT", "DELETE"])
def manage_follow(request, author_id):
    author = request.user
    follower = Author.objects.get(id=request.POST.get('follower', None))
    if author and follower:
        if request.method == "PUT":
            # accepting follow request
            follow = Follow.objects.get(user=author, follower=follower)
            follow.status = "FOLLOWED"
            follow.save()
        elif request.method == "DELETE":
            # remove follow request
            follow = Follow.objects.get(user=author, follower=follower)
            follow.delete()
        
        return Response(status=200)
    
    return Response("author and/or follower doesn't exist", status=400)


@swagger_auto_schema(
    method='get',
    operation_summary="Get list of followers",
    operation_description="""
    **When to use**: Use this endpoint to retrieve a list of followers for an author.

    **How to use**: Send a GET request with the author's ID.

    **Why/Why not**: Use this to see who is following an author.
    """,
    responses={
        200: openapi.Response(
            description="List of followers",
            examples={
                "application/json": [
                    {
                        "id": 2,
                        "username": "janedoe",
                        "display_name": "Jane Doe",
                        "github": "http://github.com/janedoe",
                        "page": "/authors/2"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def get_followers(request, author_id):
    author = Author.objects.get(id=author_id)
    followers_id = Follow.objects.filter(user=author, status="FOLLOWED").values_list('follower')
    followers = Author.objects.filter(id__in=followers_id)
    serialized_followers = [AuthorSerializer(follower).data for follower in followers]
    return Response(serialized_followers, status=200)


@swagger_auto_schema(
    method='get',
    operation_summary="Get list of following authors",
    operation_description="""
    **When to use**: Use this endpoint to retrieve a list of authors that the given author is following

    **How to use**: Send a GET request with the author's ID

    **Why/Why not**: Use this to see who the author is following
    """,
    responses={
        200: openapi.Response(
            description="List of authors the user is following",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "username": "johndoe",
                        "display_name": "John Doe",
                        "github": "http://github.com/johndoe",
                        "page": "/authors/1"   
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def get_following(request, author_id):
    author = Author.objects.get(id=author_id)
    following_ids = Follow.objects.filter(follower=author, status="FOLLOWED").values_list('user')
    following = Author.objects.filter(id__in=following_ids)
    serialized_following = [AuthorSerializer(following_user).data for following_user in following]
    return Response(serialized_following, status=200)
