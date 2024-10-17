
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Post, Like , Comment
from .serializers import CommentSerializer,PostSerializer
from .permissions import IsLocalRequest, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from urllib.parse import urlparse



User = get_user_model()

@api_view(['POST'])
def create_new_post(request,author_id):
    title = request.POST.get('title', '')
    description = request.POST.get('description', '')
    content_type = request.POST.get('contentType', '')
    content = request.POST.get('content', '')

    author = get_object_or_404(User, id=author_id)

    new_post = Post(title=title, description=description, contentType=content_type, content=content, author=author)
    new_post.save()

    serializer = PostSerializer(new_post)

    return Response(serializer.data, status=201)


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




# Helper function to get the Author object
def get_author_by_serial(serial):
    return get_object_or_404(Author, id=serial)

# Helper function to get the Post object
def get_post_by_serial(author_serial, post_serial):
    author = get_author_by_serial(author_serial)
    return get_object_or_404(Post, id=post_serial, author=author)

# Helper function to get the Comment object
def get_comment_by_serial(author_serial, post_serial, comment_serial):
    post = get_post_by_serial(author_serial, post_serial)
    return get_object_or_404(Comment, id=comment_serial, post=post)


# GET a list of likes on a post
@api_view(['GET'])
@permission_classes([AllowAny])
def get_post_likes(request, author_serial, post_serial):
    post = get_post_by_serial(author_serial, post_serial)
    likes = Like.objects.filter(object=post.get_fqid())
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

#  GET a list of likes on a post (using FQID)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_likes_by_fqid(request, post_fqid):
    likes = Like.objects.filter(object=post_fqid)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

# GET a list of likes on a comment
@api_view(['GET'])
@permission_classes([AllowAny])
def get_comment_likes(request, author_serial, post_serial, comment_serial):
    comment = get_comment_by_serial(author_serial, post_serial, comment_serial)
    likes = Like.objects.filter(object=comment.get_fqid())
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

# GET a single like by LIKE_FQID
@api_view(['GET'])
@permission_classes([AllowAny])
def get_like_by_fqid(request, like_fqid):
    like = get_object_or_404(Like, id=like_fqid)
    serializer = LikeSerializer(like)
    return Response(serializer.data)

# Function to determine if a request is local
def is_local_request(request):
    return request.get_host() == 'your-node.com'  # Replace with your domain

# Function to get Author by serial
def get_author_by_serial(serial):
    return get_object_or_404(Author, id=serial)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def author_commented(request, author_serial):
    author = get_author_by_serial(author_serial)

    if request.method == 'GET':
        return get_author_comments(request, author)
    elif request.method == 'POST':
        return post_author_comment(request, author)

def get_author_comments(request, author):
    is_local = is_local_request(request)

    if is_local:
        # Return all comments made by the author
        comments = Comment.objects.filter(author=author)
    else:
        # Return comments on public and unlisted posts
        comments = Comment.objects.filter(
            author=author,
            post__visibility__in=['PUBLIC', 'UNLISTED']
        )

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Adjust as needed
    result_page = paginator.paginate_queryset(comments, request)
    serializer = CommentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

def post_author_comment(request, author):
    if not is_local_request(request):
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data

    if data.get('type') != 'comment':
        return Response({'detail': 'Invalid type'}, status=status.HTTP_400_BAD_REQUEST)

    post_url = data.get('post')
    post_id = extract_post_id_from_url(post_url)

    if not post_id:
        return Response({'detail': 'Invalid post URL'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the post is local or remote
    try:
        post = Post.objects.get(id=post_id)
        is_local_post = True
    except Post.DoesNotExist:
        is_local_post = False

    # Save the comment
    comment = Comment(
        author=author,
        comment=data.get('comment'),
        content_type=data.get('contentType', 'text/plain'),
        published=timezone.now()
    )

    if is_local_post:
        comment.post = post
        comment.save()
        # Forward to local inbox
        recipient_author = post.author
        inbox = recipient_author.inbox
        inbox.items.append(CommentSerializer(comment).data)
        inbox.save()
    else:
        # Handle remote post
        # You might need to send the comment to the remote node
        # For now, we can save the comment without linking to a local post
        comment.save()
        # Implement logic to forward the comment to the remote node
        pass  # Replace with actual implementation

    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



def extract_post_id_from_url(post_url):
    try:
        parsed_url = urlparse(post_url)
        path_parts = parsed_url.path.strip('/').split('/')
        if 'posts' in path_parts:
            index = path_parts.index('posts')
            post_id = path_parts[index + 1]
            return post_id
        else:
            return None
    except Exception:
        return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Local requests only
def author_fqid_commented(request, author_fqid):
    if not is_local_request(request):
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    try:
        author = Author.objects.get(id=author_fqid)
    except Author.DoesNotExist:
        return Response({'detail': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(author=author)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(comments, request)
    serializer = CommentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_comment_by_serial(request, author_serial, comment_serial):
    author = get_author_by_serial(author_serial)
    comment = get_object_or_404(Comment, id=comment_serial, author=author)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Local requests only
def get_comment_by_fqid(request, comment_fqid):
    try:
        comment = Comment.objects.get(id=comment_fqid)
    except Comment.DoesNotExist:
        return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(comment)
    return Response(serializer.data)
