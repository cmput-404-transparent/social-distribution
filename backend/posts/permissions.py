# permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsLocalRequest(BasePermission):
    """
    Allows access only to local requests.

    This permission checks if the incoming request is from the local domain.
    Replace 'your-node.com' with your actual domain.
    """

    def has_permission(self, request, view):
        # Replace 'your-node.com' with your domain or use settings to get the domain dynamically
        local_domain = 'your-node.com'
        request_domain = request.get_host()
        return request_domain == local_domain

class IsRemoteRequest(BasePermission):
    """
    Allows access only to remote requests.

    This permission checks if the incoming request is not from the local domain.
    """

    def has_permission(self, request, view):
        local_domain = 'your-node.com'
        request_domain = request.get_host()
        return request_domain != local_domain

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.

    This is similar to DRF's built-in IsAuthenticatedOrReadOnly, but you can customize it here if needed.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated
        )

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.

    Assumes the model instance has an 'author' attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the object
        return obj.author == request.user

class IsAdminOrReadOnly(BasePermission):
    """
    Allows access to admin users for write operations, read-only for others.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated and request.user.is_staff
        )
