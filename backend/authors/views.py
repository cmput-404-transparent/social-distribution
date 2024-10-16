from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import *
from .serializers import AuthorSerializer
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_side_login
from rest_framework.authtoken.models import Token


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
    github = request.POST.get('github', '')
    host = request.POST.get('origin', '') + '/api/'

    if not display_name:
        display_name = username

    new_author = Author(username=username, host=host, display_name=display_name, github=github)
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

@api_view(['GET'])
def get_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    serializer = AuthorSerializer(author)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_author_from_session(request):
    session_token = request.GET.get('session')
    token_obj = Token.objects.get(key=session_token)
    return Response({'userId': token_obj.user_id}, status=200)
