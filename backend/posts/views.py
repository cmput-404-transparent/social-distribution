
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
def create_post(request, author_id):
    author = get_object_or_404(User, id=author_id)
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
def edit_post(request, author_id, post_id):
    author = get_object_or_404(User, id=author_id)
    post = get_object_or_404(Post, id=post_id, author=author)
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get a single post
@api_view(['GET'])
def get_post(request, author_id, post_id):
    """Retrieve a public post or authenticated friends-only post."""
    post = get_object_or_404(Post, id=post_id)
    if post.author.id == int(author_id):
        return Response(PostSerializer(post).data)
    else:
        # Handle visibility checks (public, friends-only) here as needed
        return Response({"detail": "Not allowed to view this post."}, status=status.HTTP_403_FORBIDDEN)


# Delete a post
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, author_id, post_id):
    """Delete an existing post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



# List recent posts by an author (paginated)
@api_view(['GET'])
def list_recent_posts(request, author_id):
    author = get_object_or_404(User, id=author_id) 

    # Get recent posts by author (paginated).
    posts = Post.objects.filter(author=author).order_by('-published')
    # Implement pagination if necessary
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
