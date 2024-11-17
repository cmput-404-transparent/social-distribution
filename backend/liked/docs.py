from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

'''
source: ChatGPT (OpenAI)
prompt: "Write me python swagger_auto_schema for this view. should be used as a decorator"
date: November 12, 2024
'''

get_like_by_fqid_docs = swagger_auto_schema(
    method='get',
    operation_summary="Get a like by fully qualified ID (fqid)",
    operation_description="""
    **When to use**: Use this endpoint to retrieve a specific like based on its fully qualified ID (fqid).

    **How to use**: Send a GET request to this endpoint with the like's fqid as a parameter.

    **Why**: This endpoint allows users to access the details of a specific like directly using its unique identifier.
    """,
    responses={
        200: openapi.Response(
            description="Like details retrieved successfully",
            examples={
                "application/json": {
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
                    "published": "2024-11-12T21:41:52.586523Z",
                    "id": "742541b4-5b43-4c3c-8d90-a1710c4cfad5",
                    "object": "http://localhost:3000/api/authors/1/posts/7122560a-9d41-4843-82ed-7273322e8c9b"
                }
            }
        ),
        404: openapi.Response(
            description="Like not found",
            examples={
                "application/json": {
                    "detail": "Not found."
                }
            }
        )
    }
)
