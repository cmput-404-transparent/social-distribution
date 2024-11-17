from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

'''
source: ChatGPT (OpenAI)
prompt: "Write me python swagger_auto_schema for this view. should be used as a decorator"
date: November 12, 2024
'''

get_comment_by_fqid_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get a comment by fully qualified ID (fqid)",
    operation_description="""
    **When to use**: Use this endpoint to retrieve a specific comment based on its fully qualified ID (fqid).

    **How to use**: Send a GET request to this endpoint with the comment's fqid as a parameter.

    **Why**: This endpoint allows users to access the details of a specific comment directly using its unique identifier.
    """,
    responses={
        200: openapi.Response(
            description="Comment details retrieved successfully",
            examples={
                "application/json": {
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
                    "comment": "everything is awesome!",
                    "contentType": "text/plain",
                    "published": "2024-11-11T08:59:36.039548Z",
                    "id": "http://localhost:3000/api/authors/1/commented/6ebb9f52-268a-49d5-9c0b-2e38436588f8",
                    "post": "http://localhost:3000/api/authors/5/posts/5a52106d-fa11-4b33-af50-04ecd5e3dd3f",
                    "page": "http://localhost:3000/api/authors/5/posts/5a52106d-fa11-4b33-af50-04ecd5e3dd3f",
                    "likes": {
                        "type": "likes",
                        "page": "http://localhost:3000/authors/1/commented/6ebb9f52-268a-49d5-9c0b-2e38436588f8/likes",
                        "id": "http://localhost:3000/api/authors/1/commented/6ebb9f52-268a-49d5-9c0b-2e38436588f8/likes",
                        "page_number": 1,
                        "size": 50,
                        "count": 0,
                        "src": []
                    }
                }
            }
        ),
        404: openapi.Response(
            description="Comment not found",
            examples={
                "application/json": {
                    "detail": "Not found."
                }
            }
        )
    }
)
