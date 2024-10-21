from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authors.models import Author, Follow  # Import Follow model
from posts.models import Post

from rest_framework.authtoken.models import Token
from unittest.mock import patch
import json

class AuthorAPITests(APITestCase):

    def setUp(self):
        self.user = Author.objects.create(username="testuser", display_name="Test User")
        self.user.set_password("testpass")  # Set password properly
        self.user.save()
        self.author = self.user  # Define self.author
        self.other_user = Author.objects.create(username="otheruser", display_name="Other User")
        self.other_user.set_password("otherpass")
        self.other_user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login(self):
        # Test the login endpoint
        url = reverse('authors:login')  # Use actual URL name with namespace
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_signup(self):
        # Test the signup endpoint
        url = reverse('authors:signup')  # Use actual URL name with namespace
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'displayName': 'New User',
            'github': 'newuser'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_get_author(self):
        # Test the get_author endpoint
        url = reverse('authors:get_author', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.author.username)

    def test_edit_author(self):
        # Test the edit_author endpoint
        url = reverse('authors:edit_author', args=[self.author.id])
        data = {'username': 'updatedauthor'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.username, 'updatedauthor')

    def test_search_author(self):
        # Test the search_author endpoint
        url = reverse('authors:search_author')
        response = self.client.get(url, {'keyword': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_follow(self):
        # Test the follow endpoint
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        url = reverse('authors:follow')
        data = {'user': self.author.id, 'follower': follower.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(user=self.author, follower=follower).exists())

    def test_get_follow_requests(self):
        # Test the get_follow_requests endpoint
        url = reverse('authors:get_follow_requests', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manage_follow(self):
        # Test the manage_follow endpoint (PUT and DELETE)
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=self.author, follower=follower, status="REQUESTED")
        url = reverse('authors:manage_follow', args=[self.author.id])
        
        # Test accepting a follow request (PUT)
        response = self.client.put(url, {'follower': follower.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        follow = Follow.objects.get(user=self.author, follower=follower)
        self.assertEqual(follow.status, 'FOLLOWED')
        
        # Test deleting a follow request (DELETE)
        response = self.client.delete(url, {'follower': follower.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(user=self.author, follower=follower).exists())

    def test_get_followers(self):
        # Test the get_followers endpoint
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=self.author, follower=follower, status="FOLLOWED")
        url = reverse('authors:get_followers', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_following(self):
        # Test the get_following endpoint
        following = Author.objects.create(username="following", display_name="Following", host="http://localhost/api/")
        Follow.objects.create(user=following, follower=self.author, status="FOLLOWED")
        url = reverse('authors:get_following', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class PostAPITests(APITestCase):

    def setUp(self):
        self.user = Author.objects.create(username="testuser", display_name="Test User")
        self.user.set_password("testpass")
        self.user.save()
        self.other_user = Author.objects.create(username="otheruser", display_name="Other User")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            content="This is the content",
            author=self.user,
            visibility="PUBLIC"
        )

    def test_create_new_post(self):
        # Test POST request to create a new post
        url = reverse('authors:create_new_post', args=[self.user.id])
        data = {
            'title': 'New Post',
            'description': 'This is a new post',
            'contentType': 'text/plain',
            'content': 'New post content',
            'visibility': 'PUBLIC'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_list_recent_posts(self):
        # Test GET request to list recent posts by an author
        url = reverse('authors:author_posts', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_post_detail(self):
        # Test GET request to retrieve a specific post
        url = reverse('authors:get_post', args=[self.user.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        # Test PUT request to update an existing post
        url = reverse('authors:get_post', args=[self.user.id, self.post.id])
        data = {'title': 'Updated Post'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_delete_post(self):
        # Test DELETE request to delete a post
        url = reverse('authors:get_post', args=[self.user.id, self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_get_all_public_posts(self):
        # Test GET request to list all public posts
        url = reverse('authors:get_public')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 1)

    def test_share_post(self):
        # Test POST request to share a post
        url = reverse('authors:share_post', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(shared_post_id=self.post.id, author=self.user).exists())

    def test_list_shared_posts(self):
        # Test GET request to list shared posts of an author
        shared_post = Post.objects.create(
            title="Shared Post",
            description="Shared post description",
            content="Shared content",
            author=self.user,
            visibility="PUBLIC",
            is_shared=True
        )
        url = reverse('authors:list_shared_posts', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_stream(self):
        # Test GET request to get a stream of posts
        Follow.objects.create(user=self.other_user, follower=self.user, status="FOLLOWED")
        other_post = Post.objects.create(
            title="Other Post",
            description="Other description",
            content="Other content",
            author=self.other_user,
            visibility="PUBLIC"
        )
        url = reverse('authors:stream', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class PostAndGithubActivityTests(APITestCase):

    def setUp(self):
        self.user = Author.objects.create(username="testuser", display_name="Test User")
        self.user.set_password("testpass")
        self.user.save()
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
        url = reverse('authors:get_post', args=[self.user.id, self.public_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Public Post')

    def test_get_friends_post_authenticated(self):
        # Test GET request to retrieve a friends-only post with authentication
        url = reverse('authors:get_post', args=[self.user.id, self.friends_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Friends Only Post')

    def test_get_friends_post_unauthenticated(self):
        # Test GET request to retrieve a friends-only post without authentication
        self.client.credentials()  # Remove authentication
        url = reverse('authors:get_post', args=[self.user.id, self.friends_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_unlisted_post(self):
        # Test GET request to retrieve an unlisted post
        url = reverse('authors:get_post', args=[self.user.id, self.unlisted_post.id])
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
        url = reverse('authors:get_post', args=[self.user.id, post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid post visibility setting", response.data['detail'])

    @patch('requests.get')  # Mocking GitHub API call
    def test_post_github_activity(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{
            'type': 'IssuesEvent',
            'id': '12345',
            'repo': {'name': 'testrepo'},
            'payload': {'action': 'opened', 'issue': {'title': 'Test Issue', 'html_url': 'http://github.com/issue/123'}},
            'created_at': '2024-01-01T12:00:00Z'
        }]

        self.user.github = "http://github.com/testuser"
        self.user.save()

        url = reverse('authors:post_github_activity', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_post = Post.objects.get(github_activity_id="12345")
        self.assertEqual(new_post.title, "testuser opened an issue")
        self.assertEqual(new_post.contentType, "text/markdown")

    @patch('requests.get')
    def test_post_github_activity_no_github_username(self, mock_get):
        # Test GET request to retrieve GitHub activity when the user has no GitHub username
        self.user.github = ""  # Empty GitHub link
        self.user.save()
        url = reverse('authors:post_github_activity', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 0)

    @patch('requests.get')
    def test_post_github_activity_no_new_events(self, mock_get):
        # Test GET request to retrieve GitHub activity with no new events
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []  # Empty list of events

        self.user.github = "http://github.com/testuser"
        self.user.save()
        url = reverse('authors:post_github_activity', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 0)  # No new posts created
