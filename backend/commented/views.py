from posts.models import Comment
from posts.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_comment_by_fqid(request, comment_fqid):
    comment = get_object_or_404(Comment, fqid=comment_fqid)
    return Response(CommentSerializer(comment).data)
