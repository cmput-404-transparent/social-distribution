
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth import get_user_model



User = get_user_model()

#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_new_post(request,author_id):
    author= get_object_or_404(User, id=author_id)
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
def update_existing_post(request, author_id, post_id):
    author = get_object_or_404(User, id=author_id)
    post = get_object_or_404(Post, id=post_id, author=author)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Get a single post
@api_view(['GET'])
def get_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id,author_id=author_id)
    return Response(PostSerializer(post).data, status=status.HTTP_200_OK)


# Delete a post
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



# List recent posts by an author (paginated), sorted by publication date
@api_view(['GET'])
def list_author_posts(request, author_id):
    author = get_object_or_404(User, id=author_id) 

    # Get recent posts by author (paginated).
    posts = Post.objects.filter(author=author).order_by('-published')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
