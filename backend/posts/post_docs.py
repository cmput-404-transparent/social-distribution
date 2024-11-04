from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

'''
source: ChatGPT (OpenAI)
prompt: "Give me a base template for Augmentating swagger doc to accomdate when how and why explanations for these views"
date: October 21, 2024s
'''

get_post_docs = swagger_auto_schema(
    method='get',
    operation_summary="Retrieve a specific post by ID",
    operation_description="""
    **When to use**: Use this endpoint to retrieve the details of a specific post by its ID and author.

    **How to use**: Send a GET request with the author's ID and post ID in the URL.

    **Why/Why not**: Need this if you want to fetch the full details of a post 
    """,
    responses={
        200: openapi.Response(
            description="Post details",
            examples={
                "application/json": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Sample Post Title",
                    "description": "A detailed description of the post",
                    "contentType": "text/plain",
                    "content": "Content of the post",
                    "author": 3,
                    "visibility": "PUBLIC",
                }
            }
        ),
        401: openapi.Response(
            description="Authentication required to view this post",
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
                    "detail": "Post not found."
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