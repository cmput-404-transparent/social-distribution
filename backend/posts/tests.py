from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authors.models import Author
from posts.models import Post
from rest_framework.authtoken.models import Token
from unittest.mock import patch

class PostAndGithubActivityTests(APITestCase):

    def setUp(self):
        # Create a user and an author for testing
        self.user = Author.objects.create(username="testuser", display_name="Test User", host="http://localhost/")
        self.other_user = Author.objects.create(username="otheruser", display_name="Other User", host="http://localhost/")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create different visibility posts for testing
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
        url = reverse('get_post', args=[self.user.id, self.public_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Public Post')

    def test_get_friends_post_authenticated(self):
        # Test GET request to retrieve a friends-only post with authentication
        url = reverse('get_post', args=[self.user.id, self.friends_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Friends Only Post')

    def test_get_friends_post_unauthenticated(self):
        # Test GET request to retrieve a friends-only post without authentication
        self.client.credentials()  # Remove authentication
        url = reverse('get_post', args=[self.user.id, self.friends_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_unlisted_post(self):
        # Test GET request to retrieve an unlisted post
        url = reverse('get_post', args=[self.user.id, self.unlisted_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Unlisted Post')

    def test_invalid_post_visibility(self):
        # Test GET request for an invalid visibility post
        post = Post.objects.create(
            title="Invalid Visibility Post",
            content="This is a post with invalid visibility",
            author=self.user,
            visibility="INVALID"
        )
        url = reverse('get_post', args=[self.user.id, post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid post visibility setting", response.data['detail'])

    @patch('requests.get')  # Mock the external GitHub API request
    def test_post_github_activity(self, mock_get):
        # Prepare a mocked response for the GitHub API
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = json.dumps([{
            'type': 'IssuesEvent',
            'id': '12345',
            'repo': {'name': 'testrepo'},
            'payload': {'action': 'opened', 'issue': {'title': 'Test Issue', 'html_url': 'http://github.com/issue/123'}},
            'created_at': '2024-01-01T12:00:00Z'
        }])

        # Test GET request to retrieve GitHub activity
        self.user.github = "http://github.com/testuser"
        self.user.save()
        url = reverse('post_github_activity', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a new post was created based on the GitHub event
        new_post = Post.objects.get(github_activity_id="12345")
        self.assertEqual(new_post.title, "testuser opened an issue")
        self.assertEqual(new_post.contentType, "text/markdown")

    @patch('requests.get')
    def test_post_github_activity_no_github_username(self, mock_get):
        # Test GET request to retrieve GitHub activity when the user has no GitHub username
        self.user.github = ""  # Empty GitHub link
        self.user.save()
        url = reverse('post_github_activity', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 0)

    @patch('requests.get')
    def test_post_github_activity_no_new_events(self, mock_get):
        # Test GET request to retrieve GitHub activity with no new events
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = json.dumps([])  # Empty list of events

        self.user.github = "http://github.com/testuser"
        self.user.save()
        url = reverse('post_github_activity', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 0)  # No new posts created
