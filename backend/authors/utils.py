import requests
from requests.auth import HTTPBasicAuth

from rest_framework import permissions
from .models import RemoteNode
from rest_framework.permissions import BasePermission

# handling outgoing requests
def send_to_remote_node(node, endpoint, data):
    url = f"{node.url.rstrip('/')}/{endpoint.lstrip('/')}"
    auth = HTTPBasicAuth(node.username, node.password)
    try:
        response = requests.post(url, json=data, auth=auth)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to {url}: {e}")
        raise
    return response

    

class IsAuthenticatedOrNode(permissions.BasePermission):
    def has_permission(self, request, view):
        print("YES!")
        # Allow if user is authenticated normally
        if isinstance(request.user, RemoteNode):
            return True
        
        # Then check for regular authenticated user
        if hasattr(request.user, 'is_authenticated'):
            return request.user.is_authenticated
            
        return False