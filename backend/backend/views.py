from django.shortcuts import render

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from authors.models import RemoteNode  # Assuming you have a RemoteNode model

from authors.models import Author
from posts.models import Post



def index(request):
    return render(request, 'index.html')
# In authors/author_views.py




# @api_view(['GET'])
# def test_remote_node_connection(request):
#     """
#     Test connection to all remote nodes or a specific remote node by its ID.
#     """
#     node_id = request.query_params.get('node_id')  # Optionally, allow testing a specific node

#     # Fetch the appropriate remote node(s)
#     if node_id:
#         remote_nodes = RemoteNode.objects.filter(id=node_id)  # Filter by specific node ID
#     else:
#         remote_nodes = RemoteNode.objects.all()  # Test all nodes

#     if not remote_nodes.exists():
#         return Response({
#             "message": "No remote nodes found to test."
#         }, status=status.HTTP_404_NOT_FOUND)

#     results = []
#     for node in remote_nodes:
#         try:
#             # Use the saved credentials for the remote node
#             response = requests.get(
#                 f"{node.url}/api/authors/",  # Example endpoint to test
#                 auth=(node.username, node.password)  # Basic Authentication
#             )
#             if response.status_code == 200:
#                 results.append({
#                     "node": node.url,
#                     "message": "Connection successful",
#                     "data": response.json()
#                 })
#             else:
#                 results.append({
#                     "node": node.url,
#                     "message": "Connection failed",
#                     "status_code": response.status_code,
#                     "details": response.text
#                 })
#         except requests.RequestException as e:
#             results.append({
#                 "node": node.url,
#                 "message": "Connection error",
#                 "error": str(e)
#             })

#     return Response(results, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_remote_node_connection(request):
    """
    Fetch authors from all connected remote nodes.
    """
    remote_nodes = RemoteNode.objects.all()  # Get all connected nodes

    if not remote_nodes.exists():
        return Response({"message": "No remote nodes found."}, status=status.HTTP_404_NOT_FOUND)

    results = []
    for node in remote_nodes:
        try:
            # Fetch authors from the remote node
            response = requests.get(
                f"{node.url}/api/authors/",
                auth=(node.username, node.password)  # Use saved credentials
            )
            if response.status_code == 200:
                results.append({
                    "node": node.url,
                    "authors": response.json()  # Add authors from this node
                })
            else:
                results.append({
                    "node": node.url,
                    "error": f"Failed with status {response.status_code}: {response.text}"
                })
        except requests.RequestException as e:
            results.append({
                "node": node.url,
                "error": str(e)
            })

    return Response(results, status=status.HTTP_200_OK)




@api_view(['GET'])
def fetch_remote_posts(request):
    """
    Fetch posts from all connected remote nodes.
    """
    remote_nodes = RemoteNode.objects.all()  # Fetch all connected nodes

    if not remote_nodes.exists():
        return Response({"message": "No remote nodes found."}, status=status.HTTP_404_NOT_FOUND)

    results = []
    for node in remote_nodes:
        try:
            # Try to fetch public posts from the remote node
            url = f"{node.url.rstrip('/')}/api/posts/public/"

            print(f"Fetching posts from: {url}")  # Debug log

            response = requests.get(url, auth=(node.username, node.password))

            if response.status_code == 200:
                posts_data = response.json()  # Assuming JSON response
                save_remote_posts(posts_data, node.url)
                results.append({
                    "node": node.url,
                    "message": f"Fetched and saved {len(posts_data)} posts.",
                })
            else:
                results.append({
                    "node": node.url,
                    "error": f"Failed with status {response.status_code}: {response.text}",
                })
        except requests.RequestException as e:
            results.append({
                "node": node.url,
                "error": str(e),
            })

    return Response(results, status=status.HTTP_200_OK)




def save_remote_posts(posts_data, node_url):
    """
    Save posts fetched from a remote node to the local database.
    """
    for post_data in posts_data:
        # Extract the post author information
        author_data = post_data.get("author", {})
        post_author, _ = Author.objects.get_or_create(
            fqid=author_data.get("id"),
            defaults={
                "host": author_data.get("host"),
                "display_name": author_data.get("displayName"),
                "github": author_data.get("github", ""),
                "profile_image": author_data.get("profileImage", ""),
                "is_remote": True,
            },
        )

        # Save or update the post in the local database
        Post.objects.update_or_create(
            fqid=post_data.get("id"),
            defaults={
                "author": post_author,
                "title": post_data.get("title", ""),
                "description": post_data.get("description", ""),
                "content": post_data.get("content", ""),
                "contentType": post_data.get("contentType", ""),
                "visibility": post_data.get("visibility", "PUBLIC"),
                "published": post_data.get("published", None),
            },
        )


