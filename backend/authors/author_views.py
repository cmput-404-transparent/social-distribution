from django.shortcuts import get_object_or_404
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from posts.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination 
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_side_login, logout as django_side_logout
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework import status
import base64
from rest_framework.decorators import authentication_classes, permission_classes
from .node_authentication import NodeBasicAuthentication
from django.utils import timezone

#documentation 
from .docs import *


@login_docs
@api_view(['POST'])
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        config = SiteConfiguration.objects.first()
        if not user.is_approved and config and config.require_user_approval:
               return Response({"detail": "Your account is pending approval."}, status=403)
        django_side_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": base64.b64encode(f"{username}:{password}".encode()), "userId": user.fqid}, status=200)
    else:
        return Response({"detail": "Invalid username or password"}, status=401)

@signup_docs
@api_view(['POST'])
def signup(request):
    config = SiteConfiguration.objects.first()
    is_approved = not config.require_user_approval if config else True

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    display_name = request.POST.get('displayName', '')
    github_username = request.POST.get('github', '')
    github_link = f"http://github.com/{github_username}"
    host = request.POST.get('origin', '') + '/api/'

    if not display_name:
        display_name = username

    new_author = Author(username=username, host=host, display_name=display_name, github=github_link, is_approved=is_approved)
    new_author.set_password(password)
    new_author.save()
    
    page = f"{request.POST.get('origin', '')}/authors/{new_author.id}"
    new_author.page = page
    new_author.save()

    if is_approved:
        user = authenticate(request, username=username, password=password)
        django_side_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": base64.b64encode(f"{username}:{password}".encode()), "userId": user.fqid}, status=201)
    else:
        return Response({"detail": "Your account is pending approval."}, status=201)

@logout_docs
@api_view(['GET'])
def logout(request):
    django_side_logout(request)
    return Response(status=200)

@get_author_by_id_docs
@api_view(['GET', 'PUT'])
def get_update_author(request, author_id):

    author = get_object_or_404(Author, pk=author_id)
    
    if request.method == 'GET':
        serializer = AuthorSummarySerializer(author, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Check if the authenticated user is the author
        if request.user.id != author.id:
            return Response({"detail": "You do not have permission to edit this profile."}, status=status.HTTP_403_FORBIDDEN)
                
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        display_name = request.data.get('displayName', None)
        profile_image = request.data.get('profileImage', None)
        github = request.data.get('github', None)

        errors = []

        if username is not None and username != author.username:
            original_username = author.username
            try:
                author.username = username
                author.save()
            except:
                author.username = original_username
                errors.append("Username is taken")
        if password is not None and password and not author.check_password(password):     # checks if passwords are the same
            author.set_password(password)           # if not then change it
        if display_name is not None and display_name != author.display_name:
            author.display_name = display_name
        if profile_image is not None and profile_image != author.profile_image:
            author.profile_image = profile_image
        if github is not None and github != author.github:
            author.github = github
        
        author.save()

        if errors:
            return Response({'errors': errors}, status=400)
        else:
            return Response(status=200)

@get_author_by_fqid_docs
@api_view(['GET'])
def get_author_by_fqid(request, author_fqid):
    author = Author.objects.filter(fqid=author_fqid)
    if author.exists():
        return Response(AuthorSummarySerializer(author.first()).data)
    return Response({"error": f"author with fqid={author_fqid} does not exist"}, status=status.HTTP_404_NOT_FOUND)

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

@get_author_docs
@api_view(['GET'])
def get_all_authors(request):
    paginator = CustomPageNumberPagination()
    authors = Author.objects.all()
    result_page = paginator.paginate_queryset(authors, request)
    serializer = AuthorSerializer(result_page, many=True)

    # format the output
    authors_data = []
    for author in serializer.data:
        author_data = {
            "type": "author",
            "id": f"{author['host']}authors/{author['id']}",
            "host": author['host'],
            "displayName": author['display_name'],
            "github": author['github'],
            "profileImage": author.get('profile_image', None),
            "page": author['page']
        }
        authors_data.append(author_data)
    
    response_data = {
        "type": "authors",
        "authors": authors_data
    }

    return Response(response_data)
    

@get_author_from_session_docs
@api_view(['GET'])
def get_author_from_session(request):
    session_token = request.GET.get('session')
    token_obj = Token.objects.get(key=session_token)
    return Response({'userId': token_obj.user_id}, status=200)


@edit_author_docs
@api_view(['POST'])
def edit_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    if request.user != author:
        return Response({"error": "Cannot modify other user's posts!"}, status=401)

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    display_name = request.POST.get('displayName', None)
    github = request.POST.get('github', None)

    errors = []

    if username is not None and username != author.username:
        original_username = author.username
        try:
            author.username = username
            author.save()
        except:
            author.username = original_username
            errors.append("Username is taken")
    if password is not None and password and not author.check_password(password):     # checks if passwords are the same
        author.set_password(password)           # if not then change it
    if display_name is not None and display_name != author.display_name:
        author.display_name = display_name
    if github is not None and github != author.github:
        author.github = github
    
    author.save()

    if errors:
        return Response({'errors': errors}, status=400)
    else:
        return Response(status=200)

@search_author_docs
@api_view(['GET'])
def search_author(request):
    keyword = request.GET.get("keyword", '')

    keyword = keyword.split("=")[1] if keyword else keyword

    results = []
    if keyword:
        results = Author.objects.filter(Q(username__icontains=keyword) | Q(display_name__icontains=keyword))
    
    results = [AuthorSerializer(author).data for author in results]

    return Response(results, status=200)


@follow_docs
@api_view(['POST'])
def follow(request):
    user = request.POST.get('user', None)
    follower = request.POST.get('follower', None)

    if user and follower:
        user_author = Author.objects.get(id=user)
        follower_author = Author.objects.get(id=follower)

        Follow.objects.get_or_create(user=user_author, follower=follower_author)

        return Response(status=201)

    else:
        return Response("user and/or follower does not exist", status=400)
    
@get_follow_request_docs
@api_view(['GET'])
def get_follow_requests(request, author_id):
    author = Author.objects.get(id=author_id)
    follow_requests = Follow.objects.filter(user=author, status="REQUESTED")
    serialized_follow_requests = [FollowRequestSerializer(follow_request).data for follow_request in follow_requests]
    response_data = {
        'type': 'followRequests',
        'src': serialized_follow_requests
    }
    return Response(response_data, status=200)


@accept_follow_docs
@delete_follow_docs
@api_view(["PUT", "DELETE"])
def manage_follow(request, author_id):
    author = request.user
    follower = Author.objects.get(id=request.POST.get('follower', None))
    if author and follower:
        if request.method == "PUT":
            # accepting follow request
            follow = Follow.objects.get(user=author, follower=follower)
            follow.status = "FOLLOWED"
            follow.save()
        elif request.method == "DELETE":
            # remove follow request
            follow = Follow.objects.get(user=author, follower=follower)
            follow.delete()
        
        return Response(status=200)
    
    return Response("author and/or follower doesn't exist", status=400)

@get_follows_docs
@api_view(['GET'])
def followers(request, author_id):
    author = Author.objects.get(id=author_id)
    followers_id = Follow.objects.filter(user=author, status="FOLLOWED").values_list('follower')
    followers = Author.objects.filter(id__in=followers_id)
    serialized_followers = [AuthorSummarySerializer(follower).data for follower in followers]
    response_data = {
        "type": "followers",
        "followers": serialized_followers
    }
    return Response(response_data, status=200)


def unfollow(request, author_id):
    following_id = request.POST.get('following', None)
    follow = get_object_or_404(Follow, user__id=following_id, follower__id=author_id)
    if follow:
        follow.delete()
    return Response(status=200)

@get_following_docs
@api_view(['GET', 'DELETE'])
def following(request, author_id):
    if request.method == 'GET':
        author = Author.objects.get(id=author_id)
        following_ids = Follow.objects.filter(follower=author, status="FOLLOWED").values_list('user')
        following = Author.objects.filter(id__in=following_ids)
        serialized_following = [AuthorSummarySerializer(following_user).data for following_user in following]
        return Response(serialized_following, status=200)
    elif request.method == 'DELETE':
        return unfollow(request, author_id)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@relationship_docs
@api_view(['GET'])
def get_relationship(request, author_1_id, author_2_id):
    author_1 = Author.objects.get(id=author_1_id)
    author_2 = Author.objects.get(id=author_2_id)
    author_serialized = AuthorSerializer(author_2, request_user=author_1)
    return Response({'relationship': author_serialized.data['relationship']}, status=200)

@api_view(['GET'])
def get_full_author(request, author_id):
    author = Author.objects.get(id=author_id)
    return Response(AuthorSerializer(author).data, status=200)

@api_view(['GET'])
def friends(request, author_id):
    author = Author.objects.get(id=author_id)
    friend_ids = Follow.get_friends(author)
    friends = Author.objects.filter(id__in=friend_ids)
    friends_serialized = [AuthorSummarySerializer(friend).data for friend in friends]
    return Response({'friends': friends_serialized}, status=200)




#view all remote node connections(GET)
# add a remote node connection(POST)
# will have to refactor acc how other groups do login 
@manage_remote_nodes_docs
@manage_remote_nodes_docs_post
@api_view(['GET','POST'])
def manage_remote_nodes(request):
    if request.method == 'GET':
        nodes = RemoteNode.objects.all()
        serializer = RemoteNodeSerializer(nodes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        url = request.data.get('host')
        username = request.data.get('username')
        password = request.data.get('password')

        if not url or not username or not password:
            return Response(
                {'detail': 'URL, username, and password are required fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = requests.post(f"{url}/api/authors/login/", data={'username': username, 'password': password} )  #(remote_node + /login)

            if response.status_code == 200:
                data = response.json()
                user_id = data.get('userId')
                token = data.get('token')  # get the tokem
                
                if not token:
                    return Response({'detail': 'Authentication token not provided by remote node.'},status=status.HTTP_400_BAD_REQUEST)                

                remote_node, created = RemoteNode.objects.update_or_create(url=url, defaults={'username': username,'token': token,})
                
                serializer = RemoteNodeSerializer(remote_node)
                return Response({"token": base64.b64encode(f"{username}:{password}".encode()), "userId": user_id}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

            else:
                return Response({'detail': 'Failed to authenticate with the remote node.'},status=response.status_code)
                
        except requests.RequestException as e:
            return Response(
                {'detail': f'Connection to remote node failed: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

def extract_author_info(actor):
    """Helper function to extract author information."""
    return {
        'fqid': actor.get('id'),
        'host': actor.get('host'),
        'display_name': actor.get('displayName'),
        'github': actor.get('github'),
        'profile_image': actor.get('profileImage'),
        'page': actor.get('page'),
        'username': actor.get('username', actor.get('id').split('/')[-1])  # Derive username if not provided
    }

@api_view(['POST'])
@authentication_classes([NodeBasicAuthentication])
def inbox(request, author_id):
    if request.method != 'POST':
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    new_item = request.data
    
    item_type = new_item.get('type')
    
    if item_type == "post":
        post_id = new_item['id']

        if not Post.objects.filter(fqid=post_id).exists():  # if post doesn't exist in db yet
            author_id = new_item['author']['id']
            host = new_item['author']['host']
            post_published = new_item.get('published', timezone.now())

            author_check = Author.objects.filter(fqid=author_id)

            if author_check:
                author = author_check.first()
            else:
                author = Author.objects.create(
                    host=host,
                    display_name=new_item['author']['displayName'],
                    username=author_id,
                    github=new_item['author']['github'],
                    profile_image=new_item['author']['profileImage'],
                    page=new_item['author']['page'],
                    fqid=author_id
                )

            new_post = Post(
                title=new_item['title'],
                description=new_item['description'],
                contentType=new_item['contentType'],
                content=new_item['content'],
                author=author,
                visibility=new_item['visibility'],
                fqid=post_id
            )
            new_post.save()
            new_post.published = post_published
            new_post.save()
        
        else:   # if post exists in db then there was an edit to the post
            post = Post.objects.get(fqid=post_id)
            post.title = new_item['title']
            post.description = new_item['description']
            post.content = new_item['content']
            post.save()

            return Response(status=status.HTTP_200_OK)

    elif item_type == "follow":
        actor_info = extract_author_info(new_item['actor'])
        object_fqid = new_item['object']['id']

        local_author = get_object_or_404(Author, fqid=object_fqid)

        remote_author_check = Author.objects.filter(fqid=actor_info['fqid'])

        if remote_author_check.exists():
            remote_author = remote_author_check.first()
        else:
            remote_author = Author.objects.create(
                host=actor_info['host'],
                display_name=actor_info['display_name'],
                username=actor_info['fqid'],
                github=actor_info['github'],
                profile_image=actor_info['profile_image'],
                page=actor_info['page'],
                fqid=actor_info['fqid'],
            )

        new_follow, created = Follow.objects.get_or_create(
            user=local_author,
            follower=remote_author,
            status="REQUESTED"
        )
        return Response(status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    elif item_type == "like":
        actor_info = extract_author_info(new_item['author'])
        object_fqid = new_item['object']
        like_id = new_item['id']
        like_published = new_item.get('published', timezone.now())

        remote_author_check = Author.objects.filter(fqid=actor_info['fqid'])

        if remote_author_check.exists():
            remote_author = remote_author_check.first()
        else:
            remote_author = Author.objects.create(
                host=actor_info['host'],
                display_name=actor_info['display_name'],
                username=actor_info['fqid'],
                github=actor_info['github'],
                profile_image=actor_info['profile_image'],
                page=actor_info['page'],
                fqid=actor_info['fqid'],
            )

        new_like, created = Like.objects.get_or_create(
            author=remote_author,
            object=object_fqid,
            fqid=like_id,
        )
        new_like.published = like_published
        new_like.save()

        return Response(status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    elif item_type == "comment":
        actor_info = extract_author_info(new_item['author'])
        comment = new_item['comment']
        content_type = new_item['contentType']
        comment_post_fqid = new_item['post']
        comment_published = new_item.get('published', timezone.now())

        remote_author_check = Author.objects.filter(fqid=actor_info['fqid'])

        if remote_author_check.exists():
            remote_author = remote_author_check.first()
        else:
            remote_author = Author.objects.create(
                host=actor_info['host'],
                display_name=actor_info['display_name'],
                username=actor_info['fqid'],
                github=actor_info['github'],
                profile_image=actor_info['profile_image'],
                page=actor_info['page'],
                fqid=actor_info['fqid'],
            )

        comment_post = get_object_or_404(Post, fqid=comment_post_fqid)

        new_comment = Comment(
            author=remote_author,
            comment=comment,
            contentType=content_type,
            post=comment_post,
        )
        new_comment.save()
        new_comment.published = comment_published
        new_comment.save()

    return Response(status=status.HTTP_201_CREATED)
