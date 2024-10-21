from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination 
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_side_login
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework import status

@api_view(['POST'])
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_side_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "userId": user.id}, status=200)
    else:
        return Response(status=401)


@api_view(['POST'])
def signup(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    display_name = request.POST.get('displayName', '')
    github_username = request.POST.get('github', '')
    github_link = f"http://github.com/{github_username}"
    host = request.POST.get('origin', '') + '/api/'

    if not display_name:
        display_name = username

    new_author = Author(username=username, host=host, display_name=display_name, github=github_link)
    new_author.set_password(password)
    new_author.save()
    
    page = f"{request.POST.get('origin', '')}/authors/{new_author.id}"
    new_author.page = page
    new_author.save()

    user = authenticate(request, username=username, password=password)
    django_side_login(request, user)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key, "userId": user.id}, status=200)


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
        if password is not None and not author.check_password(password):     # checks if passwords are the same
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


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

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
    

@api_view(['GET'])
def get_author_from_session(request):
    session_token = request.GET.get('session')
    token_obj = Token.objects.get(key=session_token)
    return Response({'userId': token_obj.user_id}, status=200)


@api_view(['GET'])
def search_author(request):
    keyword = request.GET.get("keyword", '')

    keyword = keyword.split("=")[1] if keyword else keyword

    results = []
    if keyword:
        results = Author.objects.filter(Q(username__icontains=keyword) | Q(display_name__icontains=keyword))
    
    results = [AuthorSerializer(author).data for author in results]

    return Response(results, status=200)

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

@api_view(['GET'])
def get_follow_requests(request, author_id):
    author = Author.objects.get(id=author_id)
    follow_requests = Follow.objects.filter(user=author, status="REQUESTED").values_list('follower')
    follow_requests_authors = Author.objects.filter(id__in=follow_requests)
    serialized_follow_requests = [AuthorSerializer(request).data for request in follow_requests_authors]
    return Response(serialized_follow_requests, status=200)

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

@api_view(['GET'])
def get_followers(request, author_id):
    author = Author.objects.get(id=author_id)
    followers_id = Follow.objects.filter(user=author, status="FOLLOWED").values_list('follower')
    followers = Author.objects.filter(id__in=followers_id)
    serialized_followers = [AuthorSummarySerializer(follower).data for follower in followers]
    response_data = {
        "type": "followers",
        "followers": serialized_followers
    }
    return Response(response_data, status=200)

@api_view(['GET'])
def get_following(request, author_id):
    author = Author.objects.get(id=author_id)
    following_ids = Follow.objects.filter(follower=author, status="FOLLOWED").values_list('user')
    following = Author.objects.filter(id__in=following_ids)
    serialized_following = [AuthorSummarySerializer(following_user).data for following_user in following]
    return Response(serialized_following, status=200)

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
