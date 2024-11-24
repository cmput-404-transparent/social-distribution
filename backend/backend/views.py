from sqlite3 import IntegrityError
from django.shortcuts import render
from requests.auth import HTTPBasicAuth

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from authors.models import RemoteNode  # Assuming you have a RemoteNode model

from authors.models import Author
from posts.models import Comment, Like, Post


def index(request):
    return render(request, 'index.html')


# Testing fetching authors
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
        page = 1
        while True:
            try:
                # Fetch authors from the remote node
                response = requests.get(
                    f"{node.url}/api/authors/?page={page}&size=10",
                    auth=HTTPBasicAuth(node.username, node.password)  
                )
                if response.status_code == 200:
                    authors_data = response.json().get("authors", [])
                    if not authors_data:  # Stop if no autjors 
                        break

                    # Save author
                    for author_data in authors_data:
                        author = save_remote_author(author_data)
                        if author:
                            results.append({
                                "node": node.url,
                                 "author": {
                                    "fqid": author.fqid,
                                    "display_name": author.display_name,
                                    "host": author.host,
                                    "github": author.github,
                                    "profile_image": author.profile_image,
                                },
                                "status": "saved",
                            })
                        else:
                            results.append({
                                "node": node.url,
                                "author_data": author_data,
                                "status": "failed",
                            })

                    page += 1  # next page
                else:
                    break
            except requests.RequestException as e:
                results.append({
                    "node": node.url,
                    "error": str(e)
                })
                break

    return Response(results, status=status.HTTP_200_OK)




def save_remote_author(author_data):
    """
    Save or update a remote author in the local database.
    """
    try:
        # Save or update the author based on fqid
        author, created = Author.objects.update_or_create(
            fqid=author_data.get("id"),
            defaults={
                "host": author_data.get("host"),
                "display_name": author_data.get("displayName"),
                "github": author_data.get("github", ""),
                "profile_image": author_data.get("profileImage", ""), 
                "page": author_data.get("page", ""),  # Add the page field
            },
        )
        return author  
    except IntegrityError:
        print(f"Integrity error for author: {author_data}")
        return None 

