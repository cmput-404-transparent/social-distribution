from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authors.models import Author
from posts.models import Post

from rest_framework.authtoken.models import Token
from unittest.mock import patch
import json
import base64
from urllib.parse import quote

class PostAndGithubActivityTests(APITestCase):

    def setUp(self):
        self.user = Author.objects.create(username="testuser", display_name="Test User", host="http://localhost:3000/api/")
        self.password = "testpass"
        self.user.set_password(self.password)
        self.user.save()
        self.author = self.user
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.public_post = Post.objects.create(
            title="Public Post",
            content="This is a public post",
            author=self.user,
            visibility="PUBLIC"
        )
        self.friends_post = Post.objects.create(
            title="Friends Only Post",
            content="This is a friends only post",
            author=self.user,
            visibility="FRIENDS"
        )
        self.unlisted_post = Post.objects.create(
            title="Unlisted Post",
            content="This is an unlisted post",
            author=self.user,
            visibility="UNLISTED"
        )

    def test_get_public_post(self):
        # Test GET request to retrieve a public post
        url = reverse('api:authors:get_post', args=[self.user.id, self.public_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Public Post')

    def test_get_friends_post_authenticated(self):
        # Test GET request to retrieve a friends-only post with authentication
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:get_post', args=[self.user.id, self.friends_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Friends Only Post')

    def test_get_friends_post_unauthenticated(self):
        # Test GET request to retrieve a friends-only post without authentication
        self.client.credentials()  # Remove authentication
        url = reverse('api:authors:get_post', args=[self.user.id, self.friends_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_unlisted_post(self):
        # Test GET request to retrieve an unlisted post
        url = reverse('api:authors:get_post', args=[self.user.id, self.unlisted_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Unlisted Post')

    def test_invalid_post_visibility(self):
        # Test GET request for a post with invalid visibility
        post = Post.objects.create(
            title="Invalid Visibility Post",
            content="This is a post with invalid visibility",
            author=self.user,
            visibility="INVALID"
        )
        url = reverse('api:authors:get_post', args=[self.user.id, post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid post visibility setting", response.data['detail'])

    @patch('requests.get')  # Mocking GitHub API call
    def test_post_github_activity(self, mock_get):
        mock_get.return_value.status_code = 200
        response_data = [{
            'type': 'IssuesEvent',
            'id': '12345',
            'repo': {'name': 'testrepo'},
            'payload': {'action': 'opened', 'issue': {'title': 'Test Issue', 'html_url': 'http://github.com/issue/123'}},
            'created_at': '2024-01-01T12:00:00Z'
        }]
        mock_get.return_value.content = json.dumps(response_data).encode()
        mock_get.return_value.json.return_value = response_data

        self.user.github = "http://github.com/testuser"
        self.user.save()

        url = reverse('api:posts:post_github', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_post = Post.objects.get(github_activity_id="12345")
        self.assertEqual(new_post.title, "testuser opened an issue")
        self.assertEqual(new_post.contentType, "text/markdown")

    @patch('requests.get')
    def test_post_github_activity_no_github_username(self, mock_get):
        # Test GET request to retrieve GitHub activity when the user has no GitHub username

        mock_get.return_value.status_code = 404
        response_data = []
        mock_get.return_value.content = json.dumps(response_data).encode()
        mock_get.return_value.json.return_value = response_data

        self.user.github = "http://github.com/"  # Empty GitHub link
        self.user.save()
        url = reverse('api:posts:post_github', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 3)   # no new posts create

    @patch('requests.get')
    def test_post_github_activity_no_new_events(self, mock_get):
        # Test GET request to retrieve GitHub activity with no new events
        mock_get.return_value.status_code = 200
        response_data = []
        mock_get.return_value.content = json.dumps(response_data).encode()
        mock_get.return_value.json.return_value = response_data

        self.user.github = "http://github.com/testuser"
        self.user.save()
        url = reverse('api:posts:post_github', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)  # No new posts created

    def test_get_image_post_by_fqid(self):
         # Create an image post
         with open('posts/test_image.jpg', 'rb') as image_file:
             image_content = base64.b64encode(image_file.read()).decode('utf-8')

         image_post = Post.objects.create(
             title="Image Post",
             content=image_content,
             author=self.user,
             contentType="image/jpeg;base64",
             visibility="PUBLIC"
         )

         encoded_fqid = quote(image_post.fqid, safe="")

         url = reverse('api:posts:get_image_post_by_fqid', args=[encoded_fqid])
         response = self.client.get(url)
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(response['Content-Type'], 'image/jpeg;base64')

    def test_get_non_image_post_by_fqid(self):
         encoded_fqid = quote(self.public_post.fqid, safe="")

         # Test fetching a non-image post using the image endpoint
         url = reverse('api:posts:get_image_post_by_fqid', args=[encoded_fqid])
         response = self.client.get(url)
         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
         self.assertIn("Not an image post", response.json()['detail'])
