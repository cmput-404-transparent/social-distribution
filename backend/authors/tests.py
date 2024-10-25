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
        self.password = "testpass"
        self.user.set_password(self.password)  # Set password properly
        self.user.save()
        self.author = self.user  # Define self.author
        self.other_user = Author.objects.create(username="otheruser", display_name="Other User")
        self.other_user.set_password("otherpass")
        self.other_user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login(self):
        # Test the login endpoint
        url = reverse('api:authors:login')  # Use actual URL name with namespace
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_signup(self):
        # Test the signup endpoint
        url = reverse('api:authors:signup')  # Use actual URL name with namespace
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
        url = reverse('api:authors:get_update_author', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['displayName'], self.author.display_name)

    def test_edit_author(self):
        # Test the edit_author endpoint
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:get_update_author', args=[self.author.id])
        data = {'username': 'updatedauthor'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.username, 'updatedauthor')

    def test_search_author(self):
        # Test the search_author endpoint
        url = reverse('api:authors:search_author')
        response = self.client.get(url, {'keyword': 'keyword=test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_follow(self):
        # Test the follow endpoint
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        url = reverse('api:authors:follow')
        data = {'user': self.author.id, 'follower': follower.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(user=self.author, follower=follower).exists())

    def test_get_follow_requests(self):
        # Test the get_follow_requests endpoint
        url = reverse('api:authors:get_follow_requests', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manage_follow(self):
        self.client.login(username=self.author.username, password=self.password)
        # Test the manage_follow endpoint (PUT and DELETE)
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=self.author, follower=follower, status="REQUESTED")
        url = reverse('api:authors:manage_follow', args=[self.author.id])
        
        # Test accepting a follow request (PUT)
        response = self.client.put(url, {'follower': follower.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        follow = Follow.objects.get(user=self.author, follower=follower)
        self.assertEqual(follow.status, 'FOLLOWED')
        
        # Test deleting a follow request (DELETE)
        response = self.client.delete(url, {'follower': follower.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(user=self.author, follower=follower).exists())

    def test_get_followers(self):
        # Test the get_followers endpoint
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=self.author, follower=follower, status="FOLLOWED")
        url = reverse('api:authors:followers', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['followers']), 1)
    
    def test_delete_follower(self):
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=follower, follower=self.author, status="FOLLOWED")
        url = reverse('api:authors:followers', args=[self.author.id])
        data = {'follower': follower.id}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_following(self):
        # Test the get_following endpoint
        following = Author.objects.create(username="following", display_name="Following", host="http://localhost/api/")
        Follow.objects.create(user=following, follower=self.author, status="FOLLOWED")
        url = reverse('api:authors:get_following', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class PostAPITests(APITestCase):

    def setUp(self):
        self.user = Author.objects.create(username="testuser", display_name="Test User")
        self.password = "testpass"
        self.user.set_password(self.password)
        self.user.save()
        self.author = self.user
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
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:author_posts', args=[self.user.id])
        data = {
            'title': 'New Post',
            'description': 'This is a new post',
            'contentType': 'text/plain',
            'content': 'New post content',
            'visibility': 'PUBLIC'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_list_recent_posts(self):
        # Test GET request to list recent posts by an author
        url = reverse('api:authors:author_posts', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 1)

    def test_post_detail(self):
        # Test GET request to retrieve a specific post
        url = reverse('api:authors:get_post', args=[self.user.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        # Test PUT request to update an existing post
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:get_post', args=[self.user.id, self.post.id])
        data = {'title': 'Updated Post'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_delete_post(self):
        # Test DELETE request to delete a post
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:get_post', args=[self.user.id, self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_share_post(self):
        # Test POST request to share a post
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:share_post', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(original_post=self.post.id, author=self.user).exists())

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
        url = reverse('api:authors:list_shared_posts', args=[self.user.id])
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
        url = reverse('api:authors:stream', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
