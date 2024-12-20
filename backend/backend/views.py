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
import base64

def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def remote_node_auth(request):
    try:
        remote_node = RemoteNode.objects.get(url=request.GET.get('host'))
        credentials = f"{remote_node.username}:{remote_node.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return Response({
            'credentials': encoded_credentials,
        }, status=status.HTTP_200_OK)
            
    except RemoteNode.DoesNotExist:
        return Response({'detail': 'Remote node not found.'}, status=status.HTTP_404_NOT_FOUND)

# Testing fetching authors
@api_view(['GET'])
def test_remote_node_connection(request):
    """
    Fetch authors from all connected remote nodes.
    """
    remote_nodes = RemoteNode.objects.all()  # Get all connected nodes
    if not remote_nodes.exists():
        return Response({"message": "No remote nodes found."}, status=status.HTTP_404_NOT_FOUND)

    authors_list = []
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
                        author = save_remote_author(author_data,node.url)
                        if author:
                            authors_list.append({
                                "type": "author",
                                "id": author.fqid,
                                "host": author.host,
                                "displayName": author.display_name,
                                "github": author.github,
                                "profileImage": author.profile_image,
                                "page": author.page,
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
    results = {
        "type": "authors",
        "authors": authors_list,
    }    
    return Response(results, status=status.HTTP_200_OK)




def save_remote_author(author_data,node_url=None):
    """
    Save or update a remote author in the local database.
    """
    if  "http://localhost" in author_data.get("id"):  # Skip local author
        return None
    
    elif node_url not in author_data.get('id'):
        return None
    
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
                "username": f"{author_data.get('id')}",  
            },

        )
        return author  
    except IntegrityError:
        print(f"Integrity error for author: {author_data}")
        return None 