from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import *
from .serializers import AuthorSerializer
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

    serializer = AuthorSerializer(new_author)

    return Response({"token": token.key, "author": serializer.data, "userId": user.id}, status=200)


@api_view(['GET', 'PUT'])
def get_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    
    if request.method == 'GET':
        serializer = AuthorSerializer(author, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Check if the authenticated user is the author
        if request.user.id != author.id:
            return Response({"detail": "You do not have permission to edit this profile."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AuthorSerializer(author, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

@api_view(['GET'])
def get_all_authors(request):
    paginator = CustomPageNumberPagination()
    authors = Author.objects.all()
    result_page = paginator.paginate_queryset(authors, request)
    serializer = AuthorSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
    

@api_view(['GET'])
def get_author_from_session(request):
    session_token = request.GET.get('session')
    token_obj = Token.objects.get(key=session_token)
    return Response({'userId': token_obj.user_id}, status=200)


# @api_view(['PUT'])
# def edit_author(request, author_id):
#     author = get_object_or_404(Author, pk=author_id)

#     username = request.data.get('username', None)
#     password = request.data.get('password', None)
#     display_name = request.data.get('display_name', None)
#     github = request.data.get('github', None)

#     errors = []

#     if username is not None and username != author.username:
#         original_username = author.username
#         try:
#             author.username = username
#             author.save()
#         except:
#             print('hello')
#             author.username = original_username
#             errors.append("Username is taken")
#     if password is not None and not author.check_password(password):     # checks if passwords are the same
#         author.set_password(password)           # if not then change it
#     if display_name is not None and display_name != author.display_name:
#         author.display_name = display_name
#     if github is not None and github != author.github:
#         author.github = github
    
#     author.save()

#     if errors:
#         return Response({'errors': errors}, status=400)
#     else:
#         return Response(status=200)

@api_view(['GET'])
def search_author(request):
    keyword = request.GET.get("keyword", '')

    keyword = keyword.split("=")[1] if keyword else keyword

    results = []
    if keyword:
        results = Author.objects.filter(Q(username__icontains=keyword) | Q(display_name__icontains=keyword))
    
    results = [AuthorSerializer(author).data for author in results]

    return Response(results, status=200)
