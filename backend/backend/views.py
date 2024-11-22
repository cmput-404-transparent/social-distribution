from django.shortcuts import render

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from authors.models import RemoteNode  # Assuming you have a RemoteNode model


def index(request):
    return render(request, 'index.html')
# In authors/author_views.py




@api_view(['GET'])
def test_remote_node_connection(request):
    """
    Test connection to all remote nodes or a specific remote node by its ID.
    """
    node_id = request.query_params.get('node_id')  # Optionally, allow testing a specific node

    # Fetch the appropriate remote node(s)
    if node_id:
        remote_nodes = RemoteNode.objects.filter(id=node_id)  # Filter by specific node ID
    else:
        remote_nodes = RemoteNode.objects.all()  # Test all nodes

    if not remote_nodes.exists():
        return Response({
            "message": "No remote nodes found to test."
        }, status=status.HTTP_404_NOT_FOUND)

    results = []
    for node in remote_nodes:
        try:
            # Use the saved credentials for the remote node
            response = requests.get(
                f"{node.url}/api/authors/",  # Example endpoint to test
                auth=(node.username, node.password)  # Basic Authentication
            )
            if response.status_code == 200:
                results.append({
                    "node": node.url,
                    "message": "Connection successful",
                    "data": response.json()
                })
            else:
                results.append({
                    "node": node.url,
                    "message": "Connection failed",
                    "status_code": response.status_code,
                    "details": response.text
                })
        except requests.RequestException as e:
            results.append({
                "node": node.url,
                "message": "Connection error",
                "error": str(e)
            })

    return Response(results, status=status.HTTP_200_OK)
