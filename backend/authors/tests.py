from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import * # Import all models from the authors app


class AuthorAPITests(APITestCase):

    def setUp(self):
        # Create a user and author for testing
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.author = Author.objects.create(username="testauthor", display_name="Test Author", host="http://localhost/api/")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login(self):
        # Test the login endpoint
        url = reverse('login')  # Replace with actual URL name if available
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_signup(self):
        # Test the signup endpoint
        url = reverse('signup')  # Replace with actual URL name if available
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'displayName': 'New User',
            'github': 'newuser'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_author(self):
        # Test the get_author endpoint
        url = reverse('get_author', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.author.username)

    def test_edit_author(self):
        # Test the edit_author endpoint
        url = reverse('edit_author', args=[self.author.id])
        data = {'username': 'updatedauthor'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.username, 'updatedauthor')

    def test_search_author(self):
        # Test the search_author endpoint
        url = reverse('search_author')  # Replace with actual URL name if available
        response = self.client.get(url, {'keyword': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_follow(self):
        # Test the follow endpoint
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        url = reverse('follow')  # Replace with actual URL name if available
        data = {'user': self.author.id, 'follower': follower.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(user=self.author, follower=follower).exists())

    def test_get_follow_requests(self):
        # Test the get_follow_requests endpoint
        url = reverse('get_follow_requests', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manage_follow(self):
        # Test the manage_follow endpoint (PUT and DELETE)
        follower = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=self.author, follower=follower, status="REQUESTED")
        url = reverse('manage_follow', args=[self.author.id])
        
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
        url = reverse('get_followers', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_following(self):
        # Test the get_following endpoint
        following = Author.objects.create(username="following", display_name="Following", host="http://localhost/api/")
        Follow.objects.create(user=following, follower=self.author, status="FOLLOWED")
        url = reverse('get_following', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



class PostAPITests(APITestCase):

    def setUp(self):
        # Create a user and an author for testing
        self.user = Author.objects.create(username="testuser", display_name="Test User", host="http://localhost/")
        self.other_user = Author.objects.create(username="otheruser", display_name="Other User", host="http://localhost/")
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
        url = reverse('create_new_post', args=[self.user.id])
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
        url = reverse('author_posts', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_post_detail(self):
        # Test GET request to retrieve a specific post
        url = reverse('get_post', args=[self.user.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        # Test PUT request to update an existing post
        url = reverse('get_post', args=[self.user.id, self.post.id])
        data = {'title': 'Updated Post'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_delete_post(self):
        # Test DELETE request to delete a post
        url = reverse('get_post', args=[self.user.id, self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_get_all_public_posts(self):
        # Test GET request to list all public posts
        url = reverse('get_public')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 1)

    def test_share_post(self):
        # Test POST request to share a post
        url = reverse('share_post', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Share.objects.filter(sharer=self.user, post=self.post).exists())

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
        url = reverse('list_shared_posts', args=[self.user.id])
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
        url = reverse('stream', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

