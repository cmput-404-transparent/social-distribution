from sqlite3 import IntegrityError
from django.shortcuts import render
from requests.auth import HTTPBasicAuth

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from authors.models import RemoteNode  # Assuming you have a RemoteNode model

from authors.models import Author
from posts.models import Comment, Like, Post


def index(request):
    return render(request, 'index.html')


# Testing 
@api_view(['GET'])
def test_remote_node_connection(request):  
    """
    Fetch authors from all connected remote nodes.
    """
    remote_nodes = RemoteNode.objects.all()  # Get all connected nodes

    if not remote_nodes.exists():
        return Response({"message": "No remote nodes found."}, status=status.HTTP_404_NOT_FOUND)

    results = []
    for node in remote_nodes:
        try:
            # Fetch authors from the remote node
            response = requests.get(
                f"{node.url}/api/authors/",
                auth=HTTPBasicAuth(node.username, node.password)  # Use saved credentials
            )
            if response.status_code == 200:
                results.append({
                    "node": node.url,
                    "authors": response.json()  # Add authors from this node
                })
            else:
                results.append({
                    "node": node.url,
                    "error": f"Failed with status {response.status_code}: {response.text}"
                })
        except requests.RequestException as e:
            results.append({
                "node": node.url,
                "error": str(e)
            })

    return Response(results, status=status.HTTP_200_OK)






@api_view(['GET'])
def fetch_remote_posts(request):
    """
    Fetch public posts from all connected remote nodes and save them locally.
    """
    # remote_nodes = RemoteNode.objects.all()

    remote_nodes = RemoteNode.objects.filter(is_active=True)


    if not remote_nodes.exists():
        return Response({"message": "No remote nodes found."}, status=status.HTTP_404_NOT_FOUND)

    results = []
    for node in remote_nodes:
        try:
            # Fetch posts from the remote node
            url = f"{node.url.rstrip('/')}/api/authors/posts/public/"
            print(f"Fetching posts from: {url}")

            response = requests.get(url, auth=HTTPBasicAuth(node.username, node.password))

            if response.status_code == 200:
                posts_data = response.json().get("posts", [])
                print(f"Fetched {len(posts_data)} posts from {node.url}")
                save_remote_posts(posts_data, node.url)  # Save posts locally
                results.append({
                    "node": node.url,
                    "message": f"Fetched and saved {len(posts_data)} posts.",
                })
            else:
                results.append({
                    "node": node.url,
                    "error": f"Failed with status {response.status_code}: {response.text}",
                })
        except requests.RequestException as e:
            results.append({
                "node": node.url,
                "error": str(e),
            })

    return Response(results, status=status.HTTP_200_OK)





def save_remote_posts(posts_data, node_url):
    """
    Save posts fetched from a remote node to the local database.
    """
    for post_data in posts_data:
        author_data = post_data.get("author", {})
        if not author_data:
            print(f"Invalid post data: No author found in {post_data}")
            continue

        try:
            author, created = Author.objects.get_or_create(
                fqid=author_data.get("id"),
                defaults={
                    "host": author_data.get("host"),
                    "display_name": author_data.get("displayName"),
                    "github": author_data.get("github", ""),
                    "profile_image": author_data.get("profileImage", ""),
                    "username": f"{author_data.get('host')}{author_data.get('id')}",  # Ensure unique username
                },
            )
        except IntegrityError:
            print(f"Integrity error for author: {author_data}")
            continue

        try:
            # Capture the Post object in the variable `post`
            post, _ = Post.objects.update_or_create(
                fqid=post_data.get("id"),
                defaults={
                    "author": author,
                    "title": post_data.get("title", ""),
                    "description": post_data.get("description", ""),
                    "content": post_data.get("content", ""),
                    "contentType": post_data.get("contentType", ""),
                    "visibility": post_data.get("visibility", "PUBLIC"),
                    "published": post_data.get("published"),
                },
            )
        except Exception as e:
            print(f"Error saving post {post_data.get('id')}: {e}")
            continue

        # Save likes for the post
        likes_data = post_data.get("likes", {}).get("src", [])
        for like_data in likes_data:
            try:
                like_author_data = like_data.get("author", {})
                if not like_author_data:
                    continue

                like_author, _ = Author.objects.get_or_create(
                    fqid=like_author_data.get("id"),
                    defaults={
                        "host": like_author_data.get("host"),
                        "display_name": like_author_data.get("displayName"),
                        "github": like_author_data.get("github", ""),
                        "profile_image": like_author_data.get("profileImage", ""),
                        "username": f"{like_author_data.get('host')}{like_author_data.get('id')}",
                    },
                )

                Like.objects.update_or_create(
                    fqid=like_data.get("id"),
                    defaults={
                        "author": like_author,
                        "object": post.fqid,  # Use the post's fqid as the liked object
                        "published": like_data.get("published"),
                    },
                )
            except Exception as e:
                print(f"Error saving like {like_data.get('id')}: {e}")
                continue

        # Save comments for the post
        comments_data = post_data.get("comments", {}).get("src", [])
        for comment_data in comments_data:
            try:
                comment_author_data = comment_data.get("author", {})
                if not comment_author_data:
                    continue

                comment_author, _ = Author.objects.get_or_create(
                    fqid=comment_author_data.get("id"),
                    defaults={
                        "host": comment_author_data.get("host"),
                        "display_name": comment_author_data.get("displayName"),
                        "github": comment_author_data.get("github", ""),
                        "profile_image": comment_author_data.get("profileImage", ""),
                        "username": f"{comment_author_data.get('host')}{comment_author_data.get('id')}",
                    },
                )

                Comment.objects.update_or_create(
                    fqid=comment_data.get("id"),
                    defaults={
                        "author": comment_author,
                        "post": post,
                        "comment": comment_data.get("comment"),  # Match the 'comment' field in the Comment model
                        "contentType": comment_data.get("contentType"),
                        "published": comment_data.get("published"),
                    },
                )
            except Exception as e:
                print(f"Error saving comment {comment_data.get('id')}: {e}")
                continue
