from posts.models import Like
from posts.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .docs import *

@get_like_by_fqid_docs
@api_view(['GET'])
def get_like_by_fqid(request, like_fqid):
    like = get_object_or_404(Like, fqid=like_fqid)
    return Response(LikeSerializer(like).data)
