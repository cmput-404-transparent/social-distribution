from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

'''
source: ChatGPT (OpenAI)
prompt: "Give me a base template for Augmentating swagger doc to accomdate when how and why explanations for these views"
date: October 21, 2024
'''

# Post views
create_new_post_docs = swagger_auto_schema(
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
                    "type": "post",
                    "id": "http://localhost:3000/api/authors/222/posts/249",
                    "title": "New Post Title",
                    "description": "A brief description of the post",
                    "contentType": "text/plain",
                    "content": "content of the post!",
                    "author": {
                        "type": "author",
                        "id": "http://localhost:3000/api/authors/222",
                        "host": "http://localhost:3000/api/",
                        "displayName": "Lara Cryaon",
                        "github": "http://github.com/laracroft",
                        "profileImage": "http://localhost:3000/api/authors/222/posts/217/image",
                        "page": "http://localhost:3000/authors/222"
                    },
                    "visibility": "PUBLIC"
                }
            }
        )
    }
)


# Swagger documentation for listing recent posts by an author
list_recent_posts_docs = swagger_auto_schema(
    method='get',
    operation_summary="List recent posts by a specific author",
    operation_description="""
    **When to use**: Use this endpoint to retrieve recent posts from a specific author based on visibility.

    **How to use**: Send a GET request with the author's ID to retrieve their posts.

    **Why/Why not**: Useful to use when you need to view an author's recent posts based on the specific visibility.
    """,
    responses={
        200: openapi.Response(
            description="A list of recent posts by the author",
            examples={
                "application/json": [
                    {
                        "type": "post",
                        "id": "http://localhost:3000/api/authors/222/posts/249",
                        "title": "Author's Public Post",
                        "description": "Description of the public post",
                        "contentType": "text/plain",
                        "content": "This is the content of the post.",
                        "author": {
                            "type": "author",
                            "id": "http://localhost:3000/api/authors/222",
                            "host": "http://localhost:3000/api/",
                            "displayName": "Lara Croft",
                            "github": "http://github.com/laracroft",
                            "profileImage": "http://localhost:3000/api/authors/222/posts/217/image",
                            "page": "http://localhost:3000/authors/222"
                        },
                        "visibility": "PUBLIC"
                    }
                ]
            }
        )
    }
)



update_post_docs = swagger_auto_schema(
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


delete_post_docs = swagger_auto_schema(
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

get_all_public_posts_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get all public posts from all authors",
    operation_description="""
    **When to use**: Use this endpoint to get all publicly visible posts from all authors.

    **How to use**: Send a GET request to retrieve all public posts

    **Why/Why not**: Should be used as we would to see streams of only public posts.
    """,
    responses={200: openapi.Response(
        description="A list of public posts",
        examples={
            "application/json": {
                "results": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "My First Post",
                        "description": "This is a description for my first post",
                        "contentType": "text/plain",
                        "content": "content for first page",
                        "author": {
                            "type": "author",
                            "id": "http://localhost:3000/api/authors/3",
                            "host": "http://localhost:3000/api/",
                            "displayName": "John Doe",
                            "github": "http://github.com/johndoe",
                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                            "page": "http://localhost:3000/authors/johndoe"
                        },
                        "visibility": "PUBLIC",
                    }
                ]
            }
        }
    )}
)

share_post_docs = swagger_auto_schema(
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
                    "author": {
                        "type": "author",
                        "id": "http://localhost:3000/api/authors/5",
                        "host": "http://localhost:3000/api/",
                        "displayName": "Greg Johnson",
                        "github": "http://github.com/gregjohnson",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                        "page": "http://localhost:3000/authors/greg"
                    },
                    "published": "2023-10-22T14:00:00Z",
                    "visibility": "PUBLIC",
                    "is_shared": True,
                }
            }
        ),
        403: openapi.Response(description="Forbidden: This post cannot be shared")
    }
)

list_shared_posts_docs = swagger_auto_schema(
    method='get',
    operation_summary="List all shared posts by an author",
    operation_description="""
    **When to use**: Use this endpoint to retrieve all posts shared by a specific author.

    **How to use**: Send a GET request with the author's ID in the URL. The endpoint returns shared posts that are publicly visible or, if the user is authenticated, may include additional visibility-based posts.
    """,
    responses={
        200: openapi.Response(
            description="List of shared posts",
            examples={
                "application/json": [
                    {
                        "type": "post",
                        "id": "http://localhost:3000/api/authors/3/posts/550e8400-e29b-41d4-a716-446655440000",
                        "title": "Shared: Original Post Title",
                        "description": "This is a shared post description",
                        "contentType": "text/plain",
                        "content": "This is the content of the shared post",
                        "author": {
                            "type": "author",
                            "id": "http://localhost:3000/api/authors/3",
                            "host": "http://localhost:3000/api/",
                            "displayName": "John Doe",
                            "github": "http://github.com/johndoe",
                            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                            "page": "http://localhost:3000/authors/johndoe"
                        },
                        "published": "2023-10-20T14:48:00Z",
                        "visibility": "PUBLIC",
                        "is_shared": True,
                        "original_post": "http://localhost:3000/api/authors/3/posts/550e8400-e29b-41d4-a716-446655440001"
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

stream_docs = swagger_auto_schema(
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
                            "type": "post",
                            "id": "http://localhost:3000/api/authors/3/posts/550e8400-e29b-41d4-a716-446655440000",
                            "title": "Public Post Title",
                            "description": "Description of a public post",
                            "contentType": "text/plain",
                            "content": "This is a public post",
                            "author": {
                                "type": "author",
                                "id": "http://localhost:3000/api/authors/3",
                                "host": "http://localhost:3000/api/",
                                "displayName": "John Doe",
                                "github": "http://github.com/johndoe",
                                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                                "page": "http://localhost:3000/authors/johndoe"
                            },
                            "published": "2023-10-20T14:48:00Z",
                            "visibility": "PUBLIC"
                        },
                        {
                            "type": "post",
                            "id": "http://localhost:3000/api/authors/5/posts/550e8400-e29b-41d4-a716-446655440001",
                            "title": "Unlisted Post Title",
                            "description": "Description of an unlisted post",
                            "contentType": "text/markdown",
                            "content": "This is an unlisted post",
                            "author": {
                                "type": "author",
                                "id": "http://localhost:3000/api/authors/5",
                                "host": "http://localhost:3000/api/",
                                "displayName": "Lara Croft",
                                "github": "http://github.com/laracroft",
                                "profileImage": "http://localhost:3000/api/authors/5/posts/217/image",
                                "page": "http://localhost:3000/authors/laracroft"
                            },
                            "published": "2023-10-21T10:30:00Z",
                            "visibility": "UNLISTED"
                        },
                        {
                            "type": "post",
                            "id": "http://localhost:3000/api/authors/4/posts/550e8400-e29b-41d4-a716-446655440002",
                            "title": "Friends-Only Post Title",
                            "description": "Description of a friends-only post",
                            "contentType": "text/markdown",
                            "content": "This is a friends-only post",
                            "author": {
                                "type": "author",
                                "id": "http://localhost:3000/api/authors/4",
                                "host": "http://localhost:3000/api/",
                                "displayName": "Greg Johnson",
                                "github": "http://github.com/gregjohnson",
                                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                                "page": "http://localhost:3000/authors/gregjohnson"
                            },
                            "published": "2023-10-21T11:30:00Z",
                            "visibility": "FRIENDS"
                        }
                    ]
                }
            }
        )
    }
)

# Authors views
login_docs = swagger_auto_schema(
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

# User Signup Documentation
signup_docs = swagger_auto_schema(
    method='post',
    operation_summary="User signup",
    operation_description="""
    **When to use**: Use this endpoint to create a new user account.

    **How to use**: Send a POST request with the required details (`username`, `password`, `displayName`, and `github`).

    **Why/Why not**: Use this endpoint to create a new author and log in the user.
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

# Get Author Details Documentation
get_author_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get authors",
    operation_description="""
    **When to use**: Use this endpoint to retrieve the details of all authors paginated.

    **How to use**: Send a GET request to the URL.

    **Why/Why not**: Use this to get information about an author.
    """,
    responses={
        200: openapi.Response(
            description="Author details",
            examples={
                "application/json": {
                    "type": "authors",
                    "authors": [
                        {
                            "type": "author",
                            "id": "http://localhost:3000/api/authors/1",
                            "host": "http://localhost:3000/api/",
                            "displayName": "John Doe",
                            "github": "http://github.com/JohnDoe",
                            "profileImage": "",
                            "page": "http://localhost:3000/authors/1"
                        }
                    ]
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

# get specific author documentation
author_id_param = openapi.Parameter(
    'author_id',  # The name of the parameter
    openapi.IN_PATH,  # Indicates that this parameter is in the path
    description="The ID of the author to retrieve",
    type=openapi.TYPE_INTEGER,  # Set the type of the parameter
    required=True  # Indicates that this parameter is required
)

get_author_by_id_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get author details by ID",
    operation_description="""
    **When to use**: Use this endpoint to retrieve the details of an author by their ID.

    **How to use**: Send a GET request with the author's ID in the URL.

    **Why/Why not**: Use this to get information about an author.
    """,
    manual_parameters=[author_id_param],
    responses={
        200: openapi.Response(
            description="Author details",
            examples={
                "application/json": {
                    "type": "author",
                    "id": "http://localhost:3000/api/authors/1",
                    "host": "http://localhost:3000/api/",
                    "displayName": "John Doe",
                    "github": "http://github.com/JohnDoe",
                    "profileImage": "",
                    "page": "http://localhost:3000/authors/1"
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

# Edit Author Documentation
edit_author_docs = swagger_auto_schema(
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
        200: openapi.Response(description="Author updated successfully"),
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

get_author_from_session_docs = swagger_auto_schema(
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

search_param = openapi.Parameter(
    'keywords',  # The name of the parameter
    openapi.IN_QUERY,  # Indicates that this parameter is in the path
    description="Keywords to search authors for",
    type=openapi.TYPE_STRING,  # Set the type of the parameter
    required=False  # Indicates that this parameter is required
)

search_author_docs = swagger_auto_schema(
    method='get',
    operation_summary="Search authors by keyword",
    operation_description="""
    **When to use**: Use this endpoint to search for authors by keyword.

    **How to use**: Send a GET request with the search keyword.

    **Why/Why not**: Use this to find authors by username or display name.
    """,
    manual_parameters=[search_param],
    responses={
        200: openapi.Response(
            description="Search results",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "username": "johndoe",
                        "display_name": "John Doe",
                        "github": "johndoe",
                        "page": "/authors/1"
                    }
                ]
            }
        )
    }
)

follow_docs = swagger_auto_schema(
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

get_follow_request_docs = swagger_auto_schema(
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
                        "type": "author",
                        "host": "http://localhost:3000/api/",
                        "github": "http://github.com/JohnDoe",
                        "profile_image": "",
                        "page": "http://localhost:3000/authors/6",
                        "username": "JohnDoe",
                        "display_name": "John Doe",
                        "id": "http://localhost:3000/api/authors/6",
                        "relationship": "NONE",
                        "followers": 0,
                        "following": 0
                    }
                ]
            }
        )
    }
)


accept_follow_docs = swagger_auto_schema(
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
delete_follow_docs = swagger_auto_schema(
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

get_follows_docs = swagger_auto_schema(
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
                        "type": "author",
                        "id": "http://localhost:3000/api/authors/8",
                        "host": "http://localhost:3000/api/",
                        "displayName": "User 1",
                        "github": "",
                        "profileImage": "",
                        "page": "http://localhost:3000/authors/8"
                    },
                    {
                        "type": "author",
                        "id": "http://localhost:3000/api/authors/12",
                        "host": "http://localhost:3000/api/",
                        "displayName": "User 2",
                        "github": "http://github.com/",
                        "profileImage": "",
                        "page": "http://localhost:3000/authors/12"
                    }
                ]
            }
        )
    }
)

get_following_docs = swagger_auto_schema(
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
                        "type": "author",
                        "id": "http://localhost:3000/api/authors/8",
                        "host": "http://localhost:3000/api/",
                        "displayName": "User 1",
                        "github": "",
                        "profileImage": "",
                        "page": "http://localhost:3000/authors/8"
                    },
                    {
                        "type": "author",
                        "id": "http://localhost:3000/api/authors/12",
                        "host": "http://localhost:3000/api/",
                        "displayName": "User 2",
                        "github": "http://github.com/",
                        "profileImage": "",
                        "page": "http://localhost:3000/authors/12"
                    }
                ]
            }
        )
    }
)

author_1_id_param = openapi.Parameter(
    'author_1_id',
    openapi.IN_PATH,
    description="The ID of the first author.",
    type=openapi.TYPE_INTEGER,
    required=True
)

author_2_id_param = openapi.Parameter(
    'author_2_id',
    openapi.IN_PATH,
    description="The ID of the second author.",
    type=openapi.TYPE_INTEGER,
    required=True
)

relationship_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get relationship between two authors",
    operation_description="""
    **When to use**: Use this endpoint to retrieve the relationship between two authors by their IDs.

    **How to use**: Send a GET request with the authors' IDs in the URL.

    **Why/Why not**: Use this to understand the relationship status between two authors.
    """,
    manual_parameters=[author_1_id_param, author_2_id_param],
    responses={
        200: openapi.Response(
            description="Relationship details between two authors",
            examples={
                "application/json": {
                    "relationship": "FRIEND"
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
