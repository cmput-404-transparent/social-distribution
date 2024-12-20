from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

'''
source: ChatGPT (OpenAI)
prompt: "Give me a base template for Augmentating swagger doc to accomdate when how and why explanations for these views"
date: October 21, 2024s
'''

get_post_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get a post by fully qualified ID (fqid)",
    operation_description="""
    **When to use**: Use this endpoint to retrieve a post based on its fully qualified ID (fqid).

    **How to use**: Send a GET request to this endpoint with the post's fqid as a parameter. Depending on the post's visibility setting, authentication may be required.

    **Why**: This allows users to view specific posts, respecting the post's visibility settings (PUBLIC, UNLISTED, or FRIENDS).
    """,
    responses={
        200: openapi.Response(
            description="Post details retrieved successfully",
            examples={
                "application/json": {
                    "type": "post",
                    "title": "Hello World",
                    "id": "http://localhost:3000/api/authors/7/posts/d3f29b18-3694-4348-a911-248304d83a62",
                    "page": "http://localhost:3000/authors/7/posts/d3f29b18-3694-4348-a911-248304d83a62",
                    "description": "hello everyone",
                    "contentType": "text/markdown",
                    "content": "<p>Yes</p>\n",
                    "author": {
                        "type": "author",
                        "id": "http://localhost:3000/api/authors/7",
                        "host": "http://localhost:3000/api/",
                        "displayName": "Pumpkin",
                        "github": "http://github.com/pumpkin",
                        "profileImage": "",
                        "page": "http://localhost:3000/authors/7"
                    },
                    "comments": {
                        "type": "comments",
                        "page": "http://localhost:3000/authors/7/posts/d3f29b18-3694-4348-a911-248304d83a62",
                        "id": "http://localhost:3000/api/authors/7/posts/d3f29b18-3694-4348-a911-248304d83a62/comments",
                        "page_number": 1,
                        "size": 5,
                        "count": 0,
                        "src": []
                    },
                    "likes": {
                        "type": "likes",
                        "page": "http://localhost:3000/authors/7/posts/d3f29b18-3694-4348-a911-248304d83a62",
                        "id": "http://localhost:3000/api/authors/7/posts/d3f29b18-3694-4348-a911-248304d83a62/likes",
                        "page_number": 1,
                        "size": 5,
                        "count": 0,
                        "src": []
                    },
                    "published": "2024-11-11T07:44:09.801256Z",
                    "visibility": "PUBLIC"
                }
            }
        ),
        401: openapi.Response(
            description="Authentication required for friends-only post",
            examples={
                "application/json": {
                    "detail": "Authentication required to view this post."
                }
            }
        ),
        400: openapi.Response(
            description="Invalid post visibility setting",
            examples={
                "application/json": {
                    "detail": "Invalid post visibility setting."
                }
            }
        ),
        404: openapi.Response(
            description="Post not found",
            examples={
                "application/json": {
                    "detail": "Not found."
                }
            }
        )
    }
)


post_github_activity_docs = swagger_auto_schema(
    method='get',
    operation_summary="Create posts based on GitHub activity",
    operation_description="""
    **When to use**: Use this endpoint to automatically create posts based on a user's GitHub activity.

    **How to use**: Send a GET request with the author's ID. The system will fetch the author's GitHub activity (issues, pull requests, comments) and create posts accordingly.

    **Why/Why not**: This is useful for users who want to automatically generate posts from their GitHub activity.
    """,
    responses={
        201: openapi.Response(
            description="Posts created successfully based on GitHub activity",
            examples={
                "application/json": {
                    "message": "Posts created successfully from GitHub activity."
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


get_image_post_by_fqid_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve an image post by FQID",
    operation_description="""
    **When to use**: Retrieve an image post by its Fully Qualified ID (FQID). Only publicly visible image posts are accessible through this endpoint.

    **How to use**: Send a GET request with the `post_fqid` in the URL. This endpoint checks if the post's content type is an image and decodes the base64 content to return it as a binary.

    **Why**: This endpoint allows access to publicly shared image posts by their unique FQID.
    """,
    manual_parameters=[
        openapi.Parameter(
            'post_fqid', openapi.IN_PATH, type=openapi.TYPE_STRING,
            description="Fully Qualified ID (FQID) of the post", example="http://localhost:8000/api/authors/111/posts/249"
        )
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

get_post_image_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get image from a post by fully qualified ID (fqid)",
    operation_description="""
    **When to use**: Use this endpoint to retrieve the image associated with a post by its fully qualified ID (fqid).

    **How to use**: Send a GET request to this endpoint with the post's fqid as a parameter. This endpoint will return the image source URL if the post contains an image.

    **Why**: This endpoint is designed to fetch image content from posts specifically containing images, enabling clients to display or access image posts.
    """,
    responses={
        200: openapi.Response(
            description="Image source URL retrieved successfully",
            examples={
                "application/json": {
                    "src": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAEAAId..."
                }
            }
        ),
        404: openapi.Response(
            description="Post not found or post is not an image",
            examples={
                "application/json": {
                    "error": "post is not an image post"
                }
            }
        )
    }
)

get_post_comments_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get comments for a post by fully qualified ID (fqid)",
    operation_description="""
    **When to use**: Use this endpoint to retrieve paginated comments for a specific post based on its fully qualified ID (fqid).

    **How to use**: Send a GET request to this endpoint with the post's fqid as a parameter and an optional page number query parameter (`page`). If the post visibility is 'FRIENDS', authentication is required, and users must be friends with the post author to access the comments.

    **Why**: This endpoint allows users to view comments on posts while respecting visibility settings and friendships.
    """,
    responses={
        200: openapi.Response(
            description="Paginated list of comments for the post",
            examples={
                "application/json": {
                    "type": "comments",
                    "page": "http://localhost:3000/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b",
                    "id": "http://localhost:3000/api/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b",
                    "page_number": 1,
                    "size": 5,
                    "count": 2,
                    "src": [
                        {
                            "type": "comment",
                            "author": {
                                "type": "author",
                                "id": "http://localhost:3000/api/authors/1",
                                "host": "http://localhost:3000/api/",
                                "displayName": "John Doe",
                                "github": "http://github.com/john-doe",
                                "profileImage": "http://localhost:8000/media/images/770b378e-5b36-4f9d-b81f-689275c5893e.jpeg",
                                "page": "http://localhost:3000/authors/1"
                            },
                            "comment": "hello",
                            "contentType": "text/plain",
                            "published": "2024-11-12T20:36:51.344748Z",
                            "id": "http://localhost:3000/api/authors/1/commented/c9c13eb9-8bb8-4248-b624-a20268884923",
                            "post": "http://localhost:3000/api/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b",
                            "page": "http://localhost:3000/api/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b",
                            "likes": {
                                "type": "likes",
                                "page": "http://localhost:3000/authors/1/commented/c9c13eb9-8bb8-4248-b624-a20268884923/likes",
                                "id": "http://localhost:3000/api/authors/1/commented/c9c13eb9-8bb8-4248-b624-a20268884923/likes",
                                "page_number": 1,
                                "size": 50,
                                "count": 0,
                                "src": []
                            }
                        }
                    ]
                }
            }
        ),
        401: openapi.Response(
            description="Authentication required for friends-only comments",
            examples={
                "application/json": {
                    "detail": "Authentication required to view comments."
                }
            }
        ),
        403: openapi.Response(
            description="Permission denied to view comments",
            examples={
                "application/json": {
                    "detail": "You do not have permission to view these comments."
                }
            }
        ),
        400: openapi.Response(
            description="Invalid post visibility setting",
            examples={
                "application/json": {
                    "detail": "Invalid post visibility setting."
                }
            }
        ),
        404: openapi.Response(
            description="Post not found",
            examples={
                "application/json": {
                    "detail": "Not found."
                }
            }
        )
    }
)

get_post_likes_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get likes for a post by fully qualified ID (fqid)",
    operation_description="""
    **When to use**: Use this endpoint to retrieve paginated likes for a specific post based on its fully qualified ID (fqid).

    **How to use**: Send a GET request to this endpoint with the post's fqid as a parameter, along with an optional page number query parameter (`page`) for pagination.

    **Why**: This endpoint allows users to view the likes on a specific post, providing insights into the post's engagement level.
    """,
    responses={
        200: openapi.Response(
            description="Paginated list of likes for the post",
            examples={
                "application/json": {
                    "type": "likes",
                    "page": "http://localhost:3000/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b",
                    "id": "http://localhost:3000/api/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b/likes",
                    "page_number": 1,
                    "size": 50,
                    "count": 1,
                    "src": [
                        {
                            "type": "like",
                            "author": {
                                "type": "author",
                                "id": "http://localhost:3000/api/authors/1",
                                "host": "http://localhost:3000/api/",
                                "displayName": "John Doe",
                                "github": "http://github.com/john-doe",
                                "profileImage": "http://localhost:8000/media/images/770b378e-5b36-4f9d-b81f-689275c5893e.jpeg",
                                "page": "http://localhost:3000/authors/1"
                            },
                            "published": "2024-11-12T20:43:43.441503Z",
                            "id": "7d387f4f-5ae8-45cb-a800-81af291d83b5",
                            "object": "http://localhost:3000/api/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b"
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(
            description="Post not found",
            examples={
                "application/json": {
                    "error": "post with fqid=post-fqid-example does not exist"
                }
            }
        )
    }
)
