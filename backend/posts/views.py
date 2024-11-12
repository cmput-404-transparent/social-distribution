from rest_framework.decorators import api_view, permission_classes
from authors.models import *
from .models import *
from rest_framework.response import Response
from authors.serializers import *
from posts.serializers import PostSummarySerializer
from django.shortcuts import get_object_or_404
import requests
import json
from datetime import datetime
import base64
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from urllib.parse import unquote

'''
Documentation 
source: ChatGPT (OpenAI)
prompt: "Give me a base template for Augmentating swagger doc to accomdate when how and why explanations for these views"
date: October 21, 2024
'''

# for documentation 
from .post_docs import *

@get_post_docs
@api_view(['GET'])
# Get a single post
def get_post(request, post_fqid):
    post = get_object_or_404(Post, fqid=post_fqid)

    # Public and unlisted posts are visible to everyone
    if post.visibility in ['PUBLIC', 'UNLISTED']:
        return Response(PostSummarySerializer(post).data, status=200)

    # For friends-only posts, check if the user is authenticated
    if post.visibility == 'FRIENDS':
        if request.user.is_authenticated:
            return Response(PostSummarySerializer(post).data, status=200)
        else:
            return Response({"detail": "Authentication required to view this post."}, status=401)

    # If we reach here, the post has an invalid visibility setting
    return Response({"detail": "Invalid post visibility setting."}, status=400)

@get_post_image_docs
@api_view(['GET'])
# Get the image from a post
def get_post_image(request, post_fqid):
    post = get_object_or_404(Post, fqid=post_fqid)

    if not post.contentType.startswith('image/'):
        return Response({"error": "post is not an image post"}, status=404)
    
    return Response({'src': post.content})


@post_github_activity_docs
@api_view(['GET'])
def post_github_activity(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    github_username = author.github.split("http://github.com/")[-1]

    if not github_username:
        return Response(status=200)

    response = requests.get(f"https://api.github.com/users/{github_username}/events")
    events = json.loads(response.content.decode())
    
    for event in events:
        event_type = event['type']
        payload = event['payload']
        event_id = event['id']

        # if post already exists then all subsequent posts also exist so don't need to make
        if Post.objects.filter(github_activity_id=event_id).exists():
            break

        new_post = Post()
        new_post.author = author
        new_post.contentType = 'text/markdown'
        new_post.github_activity_id = event_id

        if event_type == "IssuesEvent":
            issue = payload['issue']
            new_post.title = f"{github_username} {payload['action']} an issue"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f"<b>Issue:</b> {issue['title']}<br>View issue [here]({issue['html_url']})"

        elif event_type == "IssueCommentEvent":
            issue = payload['issue']
            comment = payload['comment']
            new_post.title = f"{github_username} commented on an issue"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f"<b>Issue:</b> {issue['title']}<br>View comment [here]({comment['html_url']})"

        elif event_type == "PullRequestEvent":
            pr = payload['pull_request']
            new_post.title = f"{github_username} {payload['action']} a pull request"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f"<b>Pull Request:</b> {issue['title']}<br>View pull request [here]({pr['html_url']})"

        elif event_type == "PullRequestReviewCommentEvent":
            pr = payload['pull_request']
            comment = payload['comment']
            new_post.title = f"{github_username} commented on a pull request"
            new_post.description = f"in {event['repo']['name']}"
            new_post.content = f"<b>Pull Request:</b> {issue['title']}<br>View comment [here]({comment['html_url']})"
        
        else:
            continue
        
        new_post.save()

        date_published = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        new_post.published = date_published
        new_post.save()

    return Response(status=201)


@get_image_post_by_fqid_docs
@api_view(['GET'])
def get_image_post_by_fqid(request, fqid):
    decoded_fqid = unquote(fqid)
    
    # Fetch the post by FQID
    post = get_object_or_404(Post, fqid=decoded_fqid, visibility='PUBLIC')

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
