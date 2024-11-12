from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from posts.serializers import *
from posts.models import *
from posts.views import get_post
from rest_framework.pagination import PageNumberPagination
from django.core.files.storage import default_storage

#documentation
from .docs import *


import base64
from django.http import HttpResponse, JsonResponse

@create_new_post_docs
@list_recent_posts_docs
# Main view that checks the request method and delegates to appropriate functions
@api_view(['GET', 'POST'])
def author_posts(request, author_id):
    if request.method == 'GET':
        return list_recent_posts(request, author_id)
    
    elif request.method == 'POST':
        return create_new_post(request, author_id)
    

# Function to handle post creation (POST)
@permission_classes([IsAuthenticated])
def create_new_post(request, author_id):

    # Check if the authenticated user matches the author_id
    if str(request.user.id) != str(author_id):
        return Response({
            "detail": "You can only create posts for yourself.",
            "your_id": str(request.user.id),
            "requested_id": author_id
        }, status=status.HTTP_403_FORBIDDEN)

    author = get_object_or_404(Author, id=author_id)

    # Handle both JSON and form data
    if request.content_type == 'application/json':
        data = request.data
    else:
        data = request.POST

    title = data.get('title', '')
    description = data.get('description', '')
    content_type = data.get('contentType', '')
    content = data.get('content', '')
    visibility = data.get('visibility', 'PUBLIC')

    # If the content includes an image URL, format it for CommonMark
    if 'image_url' in data:
        content += f"![Image]({data['image_url']})"  # Append the image URL to the content

    new_post = Post(
        title=title,
        description=description,
        contentType=content_type,
        content=content,
        author=author,
        visibility=visibility
    )
    new_post.save()

    serializer = PostSerializer(new_post)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


# # List recent posts by an author
def list_recent_posts(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    
    # Get all posts by the author
    posts = Post.objects.filter(author=author,is_deleted=False).order_by('-published')
    
    # Filter based on visibility and relationship
    if request.user.is_authenticated:
        if request.user == author:
            # Author sees all their own posts
            pass
        elif Follow.are_friends(author, request.user):
            # Friends see public, friends-only, unlisted posts, and shared posts
            posts = posts.filter(
                Q(visibility='PUBLIC') |
                Q(visibility='FRIENDS') |
                Q(visibility='UNLISTED') |
                Q(is_shared=True)
            )
        elif Follow.objects.filter(user=author, follower=request.user).exists():
            # followers can see public, unlisted posts, and shared posts
            posts = posts.filter(
                Q(visibility='PUBLIC') |
                Q(visibility='UNLISTED') |
                Q(is_shared=True)
            )
        else:
            posts = posts.filter(visibility='PUBLIC', is_shared=False)
    else:
        # Unauthenticated users see only public posts
        posts = posts.filter(visibility='PUBLIC', is_shared=False)

    # Apply pagination
    paginator = PageNumberPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)

    serializer = PostSummarySerializer(paginated_posts, many=True)

    response_data = {
        "type": "posts",
        "posts": serializer.data
    }

    return Response(response_data, status=200)


@update_post_docs
@delete_post_docs
# Main view to handle GET, PUT, and DELETE for a specific post
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, author_id, post_id):
    # author = get_object_or_404(User, id=author_id)
    post = get_object_or_404(Post, id=post_id, author_id=author_id)

    if request.method == 'GET':
        if post.visibility in ['PUBLIC', 'UNLISTED']:
            return Response(PostSummarySerializer(post).data, status=200)

        if post.visibility == 'FRIENDS':
            if request.user.is_authenticated:
                return Response(PostSummarySerializer(post).data, status=200)
            else:
                return Response({"detail": "Must be authenticated to view friends only posts."}, status=401)

        return Response({"detail": "Invalid post visibility setting."}, status=400)

    elif request.method == 'PUT':
        if request.user.is_authenticated:
            return update_existing_post(request, author_id, post_id)
        return Response({"detail": "Must be authenticated to update posts."}, status=401) 

    elif request.method == 'DELETE':
        if request.user.is_authenticated:
            return delete_post(request, author_id, post_id)
        return Response({"detail": "Must be authenticated to delete posts."}, status=401)
    


def update_existing_post(request, author_id, post_id):
    author = get_object_or_404(Author, id=author_id)
    post = get_object_or_404(Post, id=post_id, author=author)

    if request.user != author:
        return Response({"detail": "You don't have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
    data = request.data

     # For example, updating specific fields
    post.title = data.get('title', post.title)
    post.description = data.get('description', post.description)
    post.content = data.get('content', post.content)
    post.contentType = data.get('contentType', post.contentType)
    post.visibility = data.get('visibility', post.visibility)

    post.save()


    response_data = {
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'content': post.content,
        'contentType': post.contentType,
        'visibility': post.visibility,
        'published': post.published,
    } 

    return Response(response_data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
def delete_post(request, author_id, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if post.author == request.user:  # Ensure the user is the author of the post

        shared_exists = Share.objects.filter(post=post).exists()
        if shared_exists:
            shared_posts = Post.objects.filter(original_post=post)
            shared_posts.update(is_deleted=True)

        post.is_deleted = True  # Mark as deleted
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)  # Forbidden if not the author


@get_all_public_posts_docs
@api_view(['GET'])
def get_all_public_posts(request):
    public_posts = Post.objects.filter(visibility="PUBLIC").order_by('-published')
    serialized_posts = [PostSerializer(post).data for post in public_posts]
    return Response({"posts": serialized_posts}, status=200)


@share_post_docs
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if not post.is_shareable:
        return Response({"detail": "This post cannot be shared."}, status=status.HTTP_403_FORBIDDEN)
    author = post.author
    share, created = Share.objects.get_or_create(sharer=request.user, post=post)
    original_post_url = f"{author.page}/posts/{post_id}"

    shared_post_deleted = False
    shared_post_objects = Post.objects.filter(author=request.user, original_post=post)

    if not created:
        shared_post_object = shared_post_objects.first()
        shared_post_deleted = shared_post_object.is_deleted
    
    if created or shared_post_deleted:
        # Create a new post as a share
        shared_post = Post.objects.create(
            author=request.user,
            title=post.title,
            content=post.content,
            description=f"<b>{request.user.display_name} shared <a href='{original_post_url}'>{post.author.display_name}'s post</a></b>: {post.description}",
            contentType=post.contentType,
            visibility='PUBLIC',  # Ensure shared posts are always public
            is_shared=True,
            original_post=post
        )

        # if was shared before, but original post got deleted, reset the share status
        if shared_post_deleted:
            shared_post = shared_post_objects.first()
            shared_post.is_deleted = False
            shared_post.save()

        # Increment the shares count of the original post
        post.shares_count += 1
        post.save()
        post.refresh_from_db()
        return Response(PostSerializer(shared_post).data, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "You have already shared this post."}, status=status.HTTP_400_BAD_REQUEST)

@list_shared_posts_docs
@api_view(['GET'])
def list_shared_posts(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    shared_posts = Post.objects.filter(author=author, is_shared=True).order_by('-published')
    
    # Apply visibility filters similar to list_author_posts
    if request.user.is_authenticated:
        if request.user != author:
            shared_posts = shared_posts.filter(visibility='PUBLIC')
    else:
        shared_posts = shared_posts.filter(visibility='PUBLIC')
    
    serializer = PostSerializer(shared_posts, many=True)
    return Response(serializer.data)

@stream_docs
@api_view(['GET'])
def stream(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    # Initialize an empty queryset for posts
    posts = Post.objects.none()  

    # Check for public posts
    if request.user.is_authenticated:
        # Get the user's friends and followers
        following = Follow.objects.filter(follower=author, status="FOLLOWED").values_list('user', flat=True)
        friends = Follow.get_friends(author)

        # Public posts: include shared posts and also allow non-shared if the user is a follower
        public_posts = Post.objects.filter(~Q(author=author), visibility='PUBLIC')
        public_posts = public_posts.filter(Q(is_shared=True) & Q(author__in=following) | Q(is_shared=False))  # Allow public posts that are not shared

        # Add public posts to the posts queryset
        posts = posts | public_posts

        # Unlisted posts: must be shared
        following_posts = Post.objects.filter(author__in=following, visibility='UNLISTED')
        posts = posts | following_posts

        # Friends-only posts: must be shared
        friends_posts = Post.objects.filter(author__in=friends, visibility__in=['UNLISTED', 'FRIENDS'])
        posts = posts | friends_posts
    else:
        # If the user is not authenticated, include all public posts
        posts = Post.objects.filter(~Q(author=author), visibility='PUBLIC', is_shared=False)

    # Remove deleted posts
    posts = posts.exclude(is_deleted=True).order_by('-published')

    # Paginate the stream
    paginator = PageNumberPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)

    serializer = PostSummarySerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)



@get_image_post_docs
@api_view(['GET'])
def get_image_post(request, author_id, post_id):
    # Get the post by author_serial and post_serial
    post = get_object_or_404(Post, id=post_id, author_id=author_id)

    # Check if the contentType is an image
    if not post.contentType.startswith('image/'):
        return JsonResponse({"detail": "Not an image post"}, status=404)

    # Decode the base64 content to binary
    try:
        image_data = base64.b64decode(post.content)
    except base64.binascii.Error:
        return JsonResponse({"detail": "Invalid image data"}, status=400)

    # Return the image as a binary
    return HttpResponse(image_data, content_type=post.contentType)


@upload_image_docs
@api_view(['POST'])
@permission_classes([IsAdminUser])  # Restrict this to node admins
def upload_image(request):
    image_data = request.data.get('image_data')
    content_type = request.data.get('content_type', 'image/png')

    if not image_data or not image_data.startswith('data:'):
        return Response({"error": "Invalid image data"}, status=400)

    format, imgstr = image_data.split(';base64,')
    img_ext = format.split('/')[-1]
    img_data = base64.b64decode(imgstr)

    image_name = f"images/{uuid.uuid4()}.{img_ext}"
    path = default_storage.save(image_name, ContentFile(img_data))

    image_url = default_storage.url(path)  # Get URL of stored image
    return Response({"image_url": image_url}, status=201)


@get_likes_docs
@api_view(['GET'])
def get_likes(request, author_id, object_id):

    try:
        post_object = Post.objects.get(id=object_id)
        object_full_id = f"{post_object.author.page}/posts/{post_object.id}"
        object_page = f"{post_object.author.page}/posts/{post_object.id}"
    except Post.DoesNotExist:
        try:
            comment_object = Comment.objects.get(fqid=object_id)
            object_full_id = comment_object.fqid
            object_page = f"{post_object.author.page}/comments/{comment_object.fqid}/likes"
        except:
            return Response("only posts and comments have likes", status=status.HTTP_400_BAD_REQUEST)

    likes = Like.objects.filter(object=object_full_id).order_by('-published')
    paginator = Paginator(likes, 50)  # 50 likes per page
    page_number = request.query_params.get('page', 1)
    page_obj = paginator.get_page(page_number)
    serializer = LikesSerializer({
        'page': object_page,
        'id': f"{request.build_absolute_uri()}",
        'page_number': page_obj.number,
        'size': paginator.per_page,
        'count': paginator.count,
        'src': page_obj.object_list,
    })
    return Response(serializer.data)

@api_view(['GET'])
def get_comment_likes(request, author_serial, post_serial, comment_fqid):
    comment = Comment.objects.get(fqid=comment_fqid)
    object_page = f"{comment.post.author.page}/comments/{comment.id}/likes"

    likes = Like.objects.filter(object=comment.fqid).order_by('-published')
    paginator = Paginator(likes, 50)  # 50 likes per page
    if hasattr(request, 'query_params'):
        page_number = request.query_params.get('page', 1)
    elif hasattr(request, 'GET'):
        page_number = request.GET.get('page', 1)
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    serializer = LikesSerializer({
        'page': object_page,
        'id': f"{comment.fqid}/likes",
        'page_number': page_obj.number,
        'size': paginator.per_page,
        'count': paginator.count,
        'src': page_obj.object_list,
    })
    return Response(serializer.data)

@like_object_docs
@api_view(['POST'])
def like_object(request, author_id, object_id):

    author = request.user

    try:
        post_object = Post.objects.get(id=object_id)
        object_full_id = f"{post_object.author.page}/posts/{post_object.id}"
    except Post.DoesNotExist:
        try:
            comment_object = Comment.objects.get(id=object_id)
            object_full_id = comment_object.fqid
        except:
            return Response("only posts and comments have likes", status=status.HTTP_400_BAD_REQUEST)
    
    like, created = Like.objects.get_or_create(
        author=author,
        object=object_full_id,
    )
    serializer = LikeSerializer(like)
    return Response(serializer.data, status=201 if created else 200)

@send_like_to_inbox_docs
@api_view(['POST'])
def send_like_to_inbox(request, author_id):
    # Assuming you have an Inbox model
    # And an Author model with a relation to Inbox
    author = get_object_or_404(Author, id=author_id)
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        # Save the like
        serializer.save()
        # Add to inbox
        author.inbox.add(serializer.instance)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@comments_on_post_docs
@comments_on_post_post_docs
@api_view(['GET', 'POST'])
def comments_on_post(request, author_serial, post_serial):
    """
    GET: Retrieve comments on a post.
    POST: Add a comment to a post.
    """
    post = get_object_or_404(Post, id=post_serial, author__id=author_serial)

    # Handle GET request
    if request.method == 'GET':
        # Check visibility
        if post.visibility in ['PUBLIC', 'UNLISTED']:
            pass  # Anyone can see the comments
        elif post.visibility == 'FRIENDS':
            if not request.user.is_authenticated:
                return Response({"detail": "Authentication required to view comments."}, status=401)
            # Check if the user is a friend of the author
            if not Follow.are_friends(post.author, request.user):
                return Response({"detail": "You do not have permission to view these comments."}, status=403)
        else:
            return Response({"detail": "Invalid post visibility setting."}, status=400)

        comments = Comment.objects.filter(post=post).order_by('-published')
        paginator = Paginator(comments, 5)  # 5 comments per page
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        serializer = CommentsSerializer({
            'page': request.build_absolute_uri(),
            'id': f"{request.build_absolute_uri()}",
            'page_number': page_obj.number,
            'size': paginator.per_page,
            'count': paginator.count,
            'src': page_obj.object_list,
        })
        return Response(serializer.data)

    # Handle POST request
    elif request.method == 'POST':
        # Check if the user can comment on the post
        if post.visibility in ['PUBLIC', 'UNLISTED']:
            pass  # Anyone can comment
        elif post.visibility == 'FRIENDS':
            if not request.user.is_authenticated:
                return Response({"detail": "Authentication required to comment."}, status=401)
            if not Follow.are_friends(post.author, request.user):
                return Response({"detail": "You do not have permission to comment on this post."}, status=403)
        else:
            return Response({"detail": "Invalid post visibility setting."}, status=400)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, post=post)
            # Optionally, send the comment to the author's inbox here
            return Response(CommentSerializer(comment).data, status=201)
        else:
            return Response(serializer.errors, status=400)


@get_comment_docs
@api_view(['GET'])
def get_comment(request, author_serial, post_serial, comment_id):
    """
    Retrieve a specific comment on a post.
    """
    comment = get_object_or_404(Comment, id=comment_id, post__id=post_serial, post__author__id=author_serial)
    post = comment.post

    # Check visibility
    if post.visibility in ['PUBLIC', 'UNLISTED']:
        pass  # Anyone can see the comment
    elif post.visibility == 'FRIENDS':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required to view this comment."}, status=401)
        if request.user != comment.author and not Follow.are_friends(post.author, request.user):
            return Response({"detail": "You do not have permission to view this comment."}, status=403)
    else:
        return Response({"detail": "Invalid post visibility setting."}, status=400)

    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@get_author_comments_docs
@api_view(['GET'])
def get_author_comments(request, author_serial):
    """
    Retrieve comments made by an author.
    """
    author = get_object_or_404(Author, id=author_serial)

    if request.user == author:
        comments = Comment.objects.filter(author=author).order_by('-published')
    else:
        comments = Comment.objects.filter(
            author=author,
            post__visibility__in=['PUBLIC', 'UNLISTED']
        ).order_by('-published')

    paginator = Paginator(comments, 10)  # 10 comments per page
    page_number = request.query_params.get('page', 1)
    page_obj = paginator.get_page(page_number)
    serializer = CommentsSerializer({
        'page': request.build_absolute_uri(),
        'id': f"{request.build_absolute_uri()}",
        'page_number': page_obj.number,
        'size': paginator.per_page,
        'count': paginator.count,
        'src': page_obj.object_list,
    })
    return Response(serializer.data)


@get_author_comment_docs
@api_view(['GET'])
def get_author_comment(request, author_serial, comment_serial):
    """
    Retrieve a specific comment made by an author.
    """
    comment = get_object_or_404(Comment, id=comment_serial, author__id=author_serial)
    post = comment.post

    # Check visibility
    if post.visibility in ['PUBLIC', 'UNLISTED']:
        pass  # Anyone can see the comment
    elif post.visibility == 'FRIENDS':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required to view this comment."}, status=401)
        if request.user != comment.author and not Follow.are_friends(post.author, request.user):
            return Response({"detail": "You do not have permission to view this comment."}, status=403)
    else:
        return Response({"detail": "Invalid post visibility setting."}, status=400)

    serializer = CommentSerializer(comment)
    return Response(serializer.data)


@check_liked_docs
@api_view(['GET'])
def check_liked(request, author_id, post_id):
    """
    check if an author liked a post
    """
    post = get_object_or_404(Post, id=post_id)
    post_object = f"{post.author.page}/posts/{post.id}"
    liked = Like.objects.filter(author__id=author_id, object=post_object)

    return Response({"liked": liked.exists()})

@get_all_hosted_images_docs
@api_view(['GET'])
def get_all_hosted_images(request):
    """
    get all images that are hosted on this node
    """

    if request.user.is_authenticated:
        all_images = []

        _, files = default_storage.listdir('images')
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpeg')):   # images are only png or jpeg
                all_images.append("/media/images/" + file_name)

        return Response({'images': all_images}, status=200)

    return Response({'detail': 'user must be authenticated to view images on node'}, status=401)
