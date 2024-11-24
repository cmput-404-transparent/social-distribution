from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import RemoteNode
import base64

# to authenticate incoming requests from remote nodes
class NodeBasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return None

        auth_data = auth_header.split(' ')[1]
        decoded_auth = base64.b64decode(auth_data).decode('utf-8')
        username, password = decoded_auth.split(':')

        try:
            node = RemoteNode.objects.get(username=username, password=password, type="incoming", is_active=True)
        except RemoteNode.DoesNotExist:
            raise AuthenticationFailed('Invalid node credentials')

        return (node, None)
