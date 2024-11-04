from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

'''
source: ChatGPT (OpenAI)
prompt: "Give me a base template for Augmentating swagger doc to accomdate when how and why explanations for these views"
date: October 21, 2024s
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


# Retrieve all remote nodes
manage_remote_nodes_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve all registered remote nodes",
    operation_description="""
    **When to use**: Use this endpoint to retrieve a list of all registered remote nodes.

    **How to use**: Send a GET request. The response will include details for each node, such as URL, username, and token.

    **Why/Why not**: This endpoint provides administrators with an overview of all nodes that are connected.
    """,
    responses={
        200: openapi.Response(
            description="List of remote nodes",
            examples={
                "application/json": [
                    {
                        "url": "http://127.0.0.1:8000/remote-nodes",
                        "username": "admin",
                        "token": "abcd1234token"
                    },
                    {
                        "url": "http://127.0.0.1:8000/remote-nodes",
                        "username": "nodeuser",
                        "token": "token5678efgh"
                    }
                ]
            }
        ),
    }
)

# Register or update a remote node
manage_remote_nodes_docs_post = swagger_auto_schema(
    method='post',
    operation_summary="Register or update a remote node",
    operation_description="""
    **When to use**: Use this endpoint to add or update a remote node's authentication information.

    **How to use**: Send a POST request with `url`, `username`, and `password` fields. The endpoint will attempt to authenticate with the remote node using Basic Authentication and retrieve a token if successful.

    **Why/Why not**: This allows administrators to add new remote nodes and store their authentication tokens. If the node is already registered, its authentication token will be updated.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['url', 'username', 'password'],
        properties={
            'url': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The URL of the remote node.",
                example="http://127.0.0.1:8000/remote-nodes"
            ),
            'username': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The username for authentication on the remote node.",
                example="admin"
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The password for authentication on the remote node.",
                example="pass123"
            ),
        },
    ),
    responses={
        201: openapi.Response(
            description="Remote node registered successfully",
            examples={
                "application/json": {
                    "url": "http://127.0.0.1:8000/remote-nodes",
                    "username": "admin",
                    "token": "newauthtoken"
                }
            }
        ),
        200: openapi.Response(
            description="Remote node updated successfully",
            examples={
                "application/json": {
                    "url": "http://127.0.0.1:8000/remote-nodes",
                    "username": "admin",
                    "token": "updatedauthtoken"
                }
            }
        ),
        400: openapi.Response(
            description="Missing required fields",
            examples={
                "application/json": {
                    "error": "URL, username, and password are required fields."
                }
            }
        ),
        503: openapi.Response(
            description="Failed to connect to remote node",
            examples={
                "application/json": {
                    "error": "Connection to remote node failed: <error message>"
                }
            }
        )
    }
)


get_image_post_docs = swagger_auto_schema(
    method='get',
    operation_summary="get an image post",
    operation_description="""
    **When to use**: Retrieve an image post from a specific author.

    **How to use**: Send a GET request with `author_id` and `post_id` in the URL.

    **Why**: Use this endpoint to retrieve image content posts.
    """,
    manual_parameters=[
        openapi.Parameter('author_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('post_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Post ID", example="222")
    ],
    responses={
        200: openapi.Response(
            description="Image post retrieved successfully",
            examples={
                "image/jpeg": "<binary image data>"
            }
        ),
        404: openapi.Response(
            description="Not an image post",
            examples={"application/json": {"detail": "Not an image post"}}
        ),
        400: openapi.Response(
            description="Invalid image data",
            examples={"application/json": {"detail": "Invalid image data"}}
        )
    }
)


upload_image_docs = swagger_auto_schema(
    method='post',
    operation_summary="Upload an image",
    operation_description="""
    **When to use**: Upload a new image post.

    **How to use**: Send a POST request with `image_data` (base64-encoded) and `content-type`.

    **Why**: Allows admins to upload new images for authors 
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['image_data'],
        properties={
            'image_data': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The base64-encoded image data",
                example="data:image/png;base64,iVBORw0KGgoAAAANS..."
            ),
            'content_type': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The MIME type of the image",
                example="image/jpeg"
            ),
        },
    ),
    responses={
        201: openapi.Response(
            description="Image uploaded successfully",
            examples={"application/json": {"image_url": "http://localhost:8000/media/images/12345.png"}}
        ),
        400: openapi.Response(
            description="Invalid image data",
            examples={"application/json": {"error": "Invalid image data"}}
        )
    }
)

get_likes_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve likes for a post or comment",
    operation_description="""
    **When to use**: Retrieve likes on a specific post or comment.

    **How to use**: Send a GET request with `author_id` and `object_id`.

    **Why**: View the likes on a post or comment.

    supports pagination, max 50 likes per page. Use the "page" query param to navigate through the pages of likes
    """,
    manual_parameters=[
        openapi.Parameter('author_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('object_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="ID of post or comment", example="249")
    ],
    responses={
        200: openapi.Response(
            description="Likes retrieved successfully",
            examples={
                "application/json": {
                    "type": "likes",
                    "page": "http://127.0.0.1:8000/authors/222/posts/249",
                    "id": "http://127.0.0.1:8000/api/authors/222/posts/249/likes",
                    "page_number": 1,
                    "size": 50,
                    "count": 9001,
                    "src": [
                        {
                            "type": "like",
                            "author": {
                                "type": "author",
                                "id": "http://127.0.0.1:8000/api/authors/111",
                                "displayName": "Greg Johnson",
                                "github": "http://github.com/gjohnson",
                                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                            },
                            "published": "2015-03-09T13:07:04+00:00",
                            "id": "http://127.0.0.1:8000/api/authors/111/liked/166",
                            "object": "http://nodebbbb/authors/222/posts/249"
                        }
                    ]
                }
            }
        ),
        400: openapi.Response(
            description="Invalid object type",
            examples={"application/json": {"detail": "Only posts and comments have likes"}}
        )
    }
)


like_object_docs = swagger_auto_schema(
    method='post',
    operation_summary="Like a post or comment",
    operation_description="""
    **When to use**: Add a like to a post or comment.

    **How to use**: Send a POST request with `author_id` and `object_id`.

    **Why**: Allows users to have the functonality to like posts or comments
    """,
    manual_parameters=[
        openapi.Parameter('author_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('object_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="ID of post or comment to like", example="249")
    ],
    responses={
        201: openapi.Response(
            description="Like created successfully",
            examples={
                "application/json": {
                    "type": "like",
                    "id": "http://localhost:8000/api/authors/111/likes/1",
                    "author": {
                        "type": "author",
                        "id": "http://localhost:8000/api/authors/111",
                        "displayName": "Jane Doe"
                    },
                    "object": "http://localhost:8000/api/authors/111/posts/249"
                }
            }
        ),
        200: openapi.Response(
            description="Like already exists",
            examples={
                "application/json": {
                    "type": "like",
                    "id": "http://localhost:8000/api/authors/111/likes/1",
                    "author": {
                        "type": "author",
                        "id": "http://localhost:8000/api/authors/111",
                        "displayName": "Jane Doe"
                    },
                    "object": "http://localhost:8000/api/authors/111/posts/249"
                }
            }
        ),
        400: openapi.Response(
            description="Invalid object type",
            examples={"application/json": {"detail": "Only posts and comments can be liked"}}
        )
    }
)


send_like_to_inbox_docs = swagger_auto_schema(
    method='post',
    operation_summary="Send like to an author's inbox",
    operation_description="""
    **When to use**: Send a like to an author's inbox.

    **How to use**: Send a POST request with the `author_id` of the inbox owner.

    **Why**: Useful for notifying authors of likes on their content.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "type": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Type of object",
                example="like"
            ),
            "object": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The ID of the liked object",
                example="http://nodebbbb/api/authors/222/posts/249"
            )
        },
    ),
    responses={
        201: openapi.Response(
            description="Like sent to inbox",
            examples={
                "application/json": {
                    "type": "like",
                    "id": "http://localhost:8000/api/authors/111/liked/123",
                    "author": {
                        "type": "author",
                        "id": "http://localhost:8000/api/authors/111",
                        "displayName": "Jane Doe"
                    },
                    "object": "http://nodebbbb/api/authors/222/posts/249"
                }
            }
        ),
        400: openapi.Response(
            description="Invalid like data",
            examples={"application/json": {"error": "Invalid like data"}}
        )
    }
)



comments_on_post_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve comments on a post",
    operation_description="""
    **When to use**: Retrieve comments on a specific post.

    **How to use**: Send a GET request with `author_serial` and `post_serial`. This endpoint supports pagination with up to 5 comments per page.

    **Why**: Provides access to comments on posts based on visibility.
    
     Pagination  isw supported, Use the `page` query parameter to navigate through pages of comments
    """,
    manual_parameters=[
        openapi.Parameter('author_serial', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('post_serial', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Post ID", example="249"),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1, description="Page number for pagination of comments")
    ],
    responses={
        200: openapi.Response(
            description="Paginated list of comments on the post",
            examples={
                "application/json": {
                    "type": "comments",
                    "page": "http://localhost:8000/authors/222/posts/249/comments",
                    "id": "http://localhost:8000/api/authors/222/posts/249/comments",
                    "page_number": 1,
                    "size": 5,
                    "count": 25,
                    "src": [
                        {
                            "type": "comment",
                            "author": {
                                "type": "author",
                                "id": "http://localhost:8000/api/authors/111",
                                "displayName": "Greg Johnson",
                                "host":"http://localhost:8000/api/",
                                "github": "http://github.com/gjohnson",
                                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                            },
                            "comment": "Interesting post!",
                            "contentType": "text/markdown",
                            "published": "2024-11-02T13:07:04+00:00",
                            "id": "http://localhost:8000/api/authors/111/commented/130",
                            "post": "http://localhost:8000/api/authors/222/posts/249"
                        }
                    ]
                }
            }
        ),
        401: openapi.Response(description="Authentication required"),
        403: openapi.Response(description="No permission to view comments"),
        400: openapi.Response(description="Invalid post visibility setting")
    }
)

comments_on_post_post_docs = swagger_auto_schema(
    method='post',
    operation_summary="Add a comment to a post",
    operation_description="""
    **When to use**: Add a comment to a specific post.

    **How to use**: Send a POST request with the comment data. Only authenticated users with permission can comment based on the post visibility.

    **Why**: Allows users to interact with posts by commenting.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "comment": openapi.Schema(type=openapi.TYPE_STRING, description="Comment text", example="Great post!"),
            "contentType": openapi.Schema(type=openapi.TYPE_STRING, description="Content type of the comment", example="text/markdown")
        },
    ),
    responses={
        201: openapi.Response(description="Comment added successfully"),
        401: openapi.Response(description="Authentication required"),
        403: openapi.Response(description="No permission to comment on this post"),
        400: openapi.Response(description="Invalid post visibility setting")
    }
)


get_comment_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve a specific comment on a post",
    operation_description="""
    **When to use**: Retrieve a specific comment by its ID on a given post.

    **How to use**: Send a GET request with `author_serial`, `post_serial`, and `comment_id`. Visibility checks apply based on the post's visibility.

    **Why**: Useful for accessing detailed information about a single comment.
    """,
    manual_parameters=[
        openapi.Parameter('author_serial', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('post_serial', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Post ID", example="249"),
        openapi.Parameter('comment_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Comment ID", example="130")
    ],
    responses={
        200: openapi.Response(
            description="Comment retrieved successfully",
            examples={
                "application/json": {
                    "type": "comment",
                    "author": {
                        "type": "author",
                        "id": "http://localhost:8000/api/authors/111",
                        "displayName": "Greg Johnson",
                        "host":"http://localhost:8000/api/",
                        "github": "http://github.com/gjohnson",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "comment": "This is a detailed comment.",
                    "contentType": "text/markdown",
                    "published": "2024-11-02T13:07:04+00:00",
                    "id": "http://localhost:8000/api/authors/111/commented/130",
                    "post": "http://localhost:8000/api/authors/222/posts/249"
                }
            }
        ),
        401: openapi.Response(description="Authentication required"),
        403: openapi.Response(description="No permission to view this comment"),
        400: openapi.Response(description="Invalid post visibility setting")
    }
)



get_author_comments_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve comments made by a specific author",
    operation_description="""
    **When to use**: Retrieve all comments made by a given author.

    **How to use**: Send a GET request with `author_serial`. This endpoint supports pagination with up to 10 comments per page.

    **Why**: Useful for viewing a history of comments made by a particular author.

    Pagination is supported, use the `page` query parameter to navigate through pages of comments
    """,
    manual_parameters=[
        openapi.Parameter('author_serial', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1, description="Page number for pagination of comments")
    ],
    responses={
        200: openapi.Response(
            description="Paginated list of comments by the author",
            examples={
                "application/json": {
                    "type": "comments",
                    "page": "http://localhost:8000/authors/111/comments",
                    "id": "http://localhost:8000/api/authors/111/comments",
                    "page_number": 1,
                    "size": 10,
                    "count": 50,
                    "src": [
                        {
                            "type": "comment",
                            "author": {
                                "type": "author",
                                "id": "http://localhost:8000/api/authors/111",
                                "displayName": "Greg Johnson",
                                "host":"http://localhost:8000/api/",
                                "github": "http://github.com/gjohnson",
                                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                            },
                            "comment": "This is a comment on a post.",
                            "contentType": "text/plain",
                            "published": "2024-11-02T13:07:04+00:00",
                            "id": "http://localhost:8000/api/authors/111/commented/130",
                            "post": "http://localhost:8000/api/authors/222/posts/249"
                        }
                    ]
                }
            }
        ),
        401: openapi.Response(description="Authentication required")
    }
)


get_author_comment_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve a specific comment made by an author",
    operation_description="""
    **When to use**: Retrieve a specific comment made by an author on any post.

    **How to use**: Send a GET request with `author_serial` and `comment_serial`.

    **Why**: Useful for retrieving a single comment made by an author based on visibility checks.
    """,
    manual_parameters=[
        openapi.Parameter('author_serial', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('comment_serial', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Comment ID", example="130")
    ],
    responses={
        200: openapi.Response(
            description="Comment retrieved successfully",
            examples={
                "application/json": {
                    "type": "comment",
                    "author": {
                        "type": "author",
                        "id": "http://localhost:8000/api/authors/111",
                        "host":"http://localhost:8000/api/",
                        "github": "http://github.com/gjohnson",
                        "displayName": "Greg Johnson",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "comment": "Here's a detailed comment.",
                    "contentType": "text/markdown",
                    "published": "2024-11-02T13:07:04+00:00",
                    "id": "http://localhost:8000/api/authors/111/commented/130",
                    "post": "http://localhost:8000/api/authors/222/posts/249"
                }
            }
        ),
        401: openapi.Response(description="Authentication required"),
        403: openapi.Response(description="No permission to view this comment"),
        400: openapi.Response(description="Invalid post visibility setting")
    }
)


check_liked_docs = swagger_auto_schema(
    method='get',
    operation_summary="Check if an author liked a post",
    operation_description="""
    **When to use**: Use this endpoint to check if a specific author has liked a given post.

    **How to use**: Send a GET request with `author_id` and `post_id`.

    **Why**: Useful for determining if a user has interacted with a post by liking it.
    """,
    manual_parameters=[
        openapi.Parameter('author_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Author ID", example="111"),
        openapi.Parameter('post_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description="Post ID", example="249")
    ],
    responses={
        200: openapi.Response(
            description="Like status retrieved",
            examples={"application/json": {"liked": True}}
        ),
        404: openapi.Response(description="Post not found")
    }
)