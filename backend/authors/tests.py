from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authors.models import Author, Follow, RemoteNode
from posts.models import Post, Comment, Like
from authors.serializers import AuthorSummarySerializer
from posts.serializers import LikesSerializer

from rest_framework.authtoken.models import Token
from unittest.mock import patch
import json
import base64
from django.core.files.uploadedfile import SimpleUploadedFile

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
        self.admin_user = Author.objects.create(username="adminuser", password="test", display_name="Admin User", is_staff=True)
        self.admin_user.set_password(self.password)

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
    
    def test_get_all_authors(self):
        # Test the get_author endpoint
        url = reverse('api:authors:get_all_authors')
        response = self.client.get(url)
        self.assertEqual(len(response.data['authors']), 3)

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
        following = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=following, follower=self.author, status="FOLLOWED")
        url = reverse('api:authors:following', args=[self.author.id])
        data = {'following': following.id}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unfollow_friend(self):
        # make them friends (two people that follow each other)
        following = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=following, follower=self.author, status="FOLLOWED")
        Follow.objects.create(user=self.author, follower=following, status="FOLLOWED")

        self.assertTrue(Follow.are_friends(following, self.author))

        url = reverse('api:authors:following', args=[self.author.id])
        data = {'following': following.id}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.are_friends(following, self.author))

    def test_get_following(self):
        # Test the get_following endpoint
        following = Author.objects.create(username="following", display_name="Following", host="http://localhost/api/")
        Follow.objects.create(user=following, follower=self.author, status="FOLLOWED")
        url = reverse('api:authors:following', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_friends(self):
        # make them friends (two people that follow each other)
        following = Author.objects.create(username="follower", display_name="Follower", host="http://localhost/api/")
        Follow.objects.create(user=following, follower=self.author, status="FOLLOWED")
        Follow.objects.create(user=self.author, follower=following, status="FOLLOWED")

        self.assertTrue(Follow.are_friends(following, self.author))

        url = reverse('api:authors:friends', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['friends']), 1)
    
    def get_remote_nodes(self):
        self.client.login(username=self.admin_user.username, password=self.password)
        RemoteNode.objects.create(url="http://localhost:3000", username="test_username", password=self.password)
        url = reverse('api:authors:friends', args=[self.author.id])
        response = self.client.get(url)
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
        self.assertTrue(Post.objects.get(id=self.post.id).is_deleted)
    
    def test_no_deleted_posts_on_stream(self):
        # test that you can't see deleted posts on stream
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:stream', args=[self.author.id])
        Post.objects.create(
            title="Deleted Post",
            description="Deleted post description",
            content="Deleted post content",
            author=self.other_user,
            visibility="PUBLIC",
            is_deleted=True
        )
        response = self.client.get(url).json()
        self.assertEqual(response['count'], 0)

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

class CommentsLikesImagesAPITests(APITestCase):

    def setUp(self):
        self.user = Author.objects.create(username="testuser", display_name="Test User", host="http://localhost:3000/api/")
        self.password = "testpass"
        self.user.set_password(self.password)
        self.user.save()
        self.author = self.user
        self.other_user = Author.objects.create(username="otheruser", display_name="Other User", host="http://localhost:3000/api/")
        self.other_user.set_password("otherpass")
        self.other_user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            content="This is the content",
            author=self.user,
            visibility="PUBLIC"
        )
        # Create an admin user for testing admin-only views
        self.admin_user = Author.objects.create(username="adminuser", display_name="Admin User", is_staff=True)
        self.admin_user.set_password(self.password)
        self.admin_user.save()
        self.admin_token = Token.objects.create(user=self.admin_user)

    # Existing test methods remain the same

    def test_upload_image(self):
        # Test POST request to upload an image
        self.client.login(username=self.admin_user.username, password=self.password)
        url = reverse('api:authors:upload_image')
        image_content = base64.b64encode(b'test image content').decode('utf-8')
        image_data = f'data:image/png;base64,{image_content}'
        data = {
            'image_data': image_data,
            'content_type': 'image/png'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('image_url', response.data)

    def test_get_image_post(self):
        # Test GET request to retrieve an image post
        image_content = base64.b64encode(b'test image content').decode('utf-8')
        image_post = Post.objects.create(
            title="Image Post",
            description="An image post",
            content=image_content,
            contentType="image/png",
            author=self.user,
            visibility="PUBLIC"
        )
        url = reverse('api:authors:get_image_post', args=[self.user.id, image_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertEqual(response.content, base64.b64decode(image_content))

    def test_get_likes(self):
        # Test GET request to retrieve likes on a post
        Like.objects.create(author=self.user, object=self.post.fqid)
        url = reverse('api:authors:get_likes', args=[self.user.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_like_object(self):
        # Test POST request to like a post
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:like_object', args=[self.user.id, self.post.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertTrue(Like.objects.filter(author=self.user, object=self.post.fqid).exists())

    def test_comments_on_post_get(self):
        # Test GET request to retrieve comments on a post
        Comment.objects.create(
            author=self.other_user,
            post=self.post,
            comment="Test Comment"
        )
        url = reverse('api:authors:comments_on_post', args=[self.user.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['src']), 1)

    def test_comments_on_post_post(self):
        # Test POST request to add a comment to a post
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:comments_on_post', args=[self.user.id, self.post.id])
        data = {
            'comment': 'This is a test comment'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.user, comment='This is a test comment').exists())

    def test_get_comment(self):
        # Test GET request to retrieve a specific comment
        comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            comment="Test Comment"
        )
        url = reverse('api:authors:get_comment', args=[self.user.id, self.post.id, comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], 'Test Comment')

    def test_get_author_comments(self):
        # Test GET request to retrieve comments made by an author
        Comment.objects.create(
            author=self.user,
            post=self.post,
            comment="Test Comment"
        )
        url = reverse('api:authors:get_author_comments', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['src']), 1)

    def test_get_author_comment(self):
        # Test GET request to retrieve a specific comment made by an author
        comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            comment="Test Comment"
        )
        url = reverse('api:authors:get_author_comment', args=[self.user.id, comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], 'Test Comment')

    def test_check_liked(self):
        # Test GET request to check if an author liked a post
        Like.objects.create(
            author=self.user,
            object=self.post.fqid
        )
        url = reverse('api:authors:check_liked', args=[self.user.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['liked'])

    def test_get_all_hosted_images(self):
        # Test GET request to get all hosted images
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:get_all_hosted_images')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('images', response.data)

    def test_get_all_public_posts(self):
        # Test GET request to get all public posts
        Post.objects.create(
            title="Public Post",
            description="Public post description",
            content="Public content",
            author=self.other_user,
            visibility="PUBLIC"
        )
        url = reverse('api:authors:get_all_public_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 2)


class PostFeatureTests(APITestCase):

    def setUp(self):
        self.user = Author.objects.create(username="testuser", display_name="Test User")

        self.password = "testpass"
        self.user.set_password(self.password)
        self.user.save()
        self.author = self.user
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        oldPost = Post.objects.create(

            title="Older Post",
            description="Older description",
            content="Older content",
            author=self.author,
            visibility="PUBLIC",
            published="2024-01-01T00:00:00Z"
        )

        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            content="This is the content",
            author=self.user,
            visibility="PUBLIC"
        )
        self.friends_Only = Post.objects.create(
            title="Friends Only Post",
            description="Friends only content",
            content="Visible only to friends",
            author=self.author,
            visibility="FRIENDS"
        )
        url = reverse('api:authors:stream', args=[self.author.id])
        response = self.client.get(url)
    
    # PostingTests


    def test_post_creation_with_commonmark(self):
        self.client.login(username=self.user.username, password=self.password)
        url = reverse('api:authors:author_posts', args=[self.user.id])
        data = {
            'title': 'CommonMark Post',
            'description': 'Post with CommonMark',
            'contentType': 'text/markdown',
            'content': '# Heading\n\nThis is a **bold** statement.',
            'visibility': 'PUBLIC'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['contentType'], 'text/markdown')

    def test_edit_post_and_resend(self):
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:get_post', args=[self.user.id, self.post.id])
        data = {'title': 'Updated Title', 'content': 'Updated content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Mock the behavior of re-sending the post update
        # with patch('posts.models.Post.send_update') as mocked_send_update:    # TODO: not implemented yet
        #     self.post.refresh_from_db()
        #     mocked_send_update.assert_called_once()

    def test_post_deletion_and_notification(self):
        self.client.login(username=self.user.username, password=self.password)
        url = reverse('api:authors:get_post', args=[self.user.id, self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Mock the behavior of notifying nodes
        # with patch('posts.models.Post.send_deletion_notice') as mocked_deletion_notice:   # TODO: not implemented yet
        #     mocked_deletion_notice.assert_called_once()


    def test_delete_other_authors_post(self):
        other_author = Author.objects.create(username="otheruser2", display_name="Other User2")
        post_by_other = Post.objects.create(
            title="Other Author's Post",
            description="Other content",
            content="This is other author's content",
            author=other_author,
            visibility="PUBLIC"
        )
        url = reverse('api:authors:get_post', args=[other_author.id, post_by_other.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # Test for reading of posts
    def test_stream_includes_edited_posts(self):
        self.client.login(username=self.author.username, password=self.password)
        self.post.title = "Edited Post"
        self.post.save()
        other_author = Author.objects.create(username="otherauthor", display_name="otherauthor")
        url = reverse('api:authors:stream', args=[other_author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Edited Post', str(response.content))


    def test_stream_sorting(self):
        other_author2 = Author.objects.create(username="otheruser6", display_name="Other User6")
        other_author2.set_password(self.password)
        other_author2.save()
        self.client.login(username=self.author.username, password=self.password)
        url = reverse('api:authors:stream', args=[other_author2.id])
        response = self.client.get(url)
        data = json.loads(response.content)
        posts = [p['title'] for p in data['results']]
        self.assertEqual(posts, ["Test Post", "Older Post"])

    def test_visibility_friends_only(self):
        other_author = Author.objects.create(username="otheruser5", display_name="Other User5")
        other_author2 = Author.objects.create(username="otheruser6", display_name="Other User6")
        other_author2.set_password(self.password)
        other_author2.save()
        Follow.objects.create(user=other_author2, follower=other_author, status="FOLLOWED")
        Follow.objects.create(user=other_author, follower=other_author2, status="FOLLOWED")
        post = Post(
            title="Otheruser 5 Post",
            description="Other content",
            content="This is other author's content",
            author=other_author,
            visibility="FRIENDS"
        )
        post.save()
        self.client.login(username=other_author2.username, password=self.password)
        url = reverse('api:authors:stream', args=[other_author2.id])
        response = self.client.get(url)
        self.assertIn("Otheruser 5 Post", str(response.content))

    # Test for visibility of posts
    def test_make_post_public(self):
        self.post.visibility = "PUBLIC"
        self.post.save()
        self.assertEqual(self.post.visibility, "PUBLIC")

    def test_unlisted_post_access_by_link(self):
        self.post.visibility = "UNLISTED"
        self.post.save()
        url = reverse('api:authors:get_post', args=[self.author.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restricted_access_to_friends_only_post(self):
        self.post.visibility = "FRIENDS"
        self.post.save()
        url = reverse('api:authors:get_post', args=[self.post.author.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_stream_excludes_deleted_posts(self):
        self.post.is_deleted = True
        self.post.save()
        url = reverse('api:authors:stream', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.post.title, str(response.content))


class InboxTests(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(username="testuser", display_name="Test User")
        self.password = "testpass"
        self.author.set_password(self.password)
        self.author.save()

        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            content="This is the content",
            author=self.author,
            visibility="PUBLIC"
        )

    def test_send_posts_to_remote_followers(self):
        url = reverse('api:authors:inbox', args=[self.author.id])
        post_id = "http://nodebbbb/api/authors/222/posts/249"
        title = "A post title about a post about web dev"

        post_object = {
            "type": "post",
            "title": title,
            "id": post_id,
            "page": "http://nodebbbb/authors/222/posts/293",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "This is a short post about web development.",
            "author": {
                "type": "author",
                "id": "http://nodebbbb/api/authors/222",
                "host": "http://nodebbbb/api/",
                "displayName": "Lara Croft",
                "page": "http://nodebbbb/authors/222",
                "github": "http://github.com/laracroft",
                "profileImage": "http://nodebbbb/api/authors/222/posts/217/image"
            },
            "likes": {
                "type": "likes",
                "page": "http://nodeaaaa/authors/222/posts/249",
                "id": "http://nodeaaaa/api/authors/222/posts/249/likes",
                "page_number": 1,
                "size": 50,
                "count": 9001,
                "src": [
                {
                    "type": "like",
                    "author": {
                    "type": "author",
                    "id": "http://nodeaaaa/api/authors/111",
                    "page": "http://nodeaaaa/authors/greg",
                    "host": "http://nodeaaaa/api/",
                    "displayName": "Greg Johnson",
                    "github": "http://github.com/gjohnson",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "published": "2015-03-09T13:07:04+00:00",
                    "id": "http://nodeaaaa/api/authors/111/liked/166",
                    "object": "http://nodebbbb/authors/222/posts/249"
                }
                ]
            },
            "published": "2015-03-09T13:07:04+00:00",
            "visibility": "PUBLIC"
        }

        response = self.client.post(url, post_object, format='json')
        new_post = Post.objects.filter(fqid=post_id)
        self.assertTrue(new_post.exists())      # check for the id
        new_post = new_post.first()
        self.assertEqual(new_post.title, title)     # check for the title
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_resend_edited_posts(self):
        url = reverse('api:authors:inbox', args=[self.author.id])
        new_title = "A new post title about a post about web dev"
        post_id = self.post.fqid

        likes = LikesSerializer({
            'page': self.post.page,
            'id': self.post.fqid + "/likes",
            'page_number': 1,
            'size': 5,
            'count': 0,
            'src': [],
        }).data

        post_object = {     # post object version of self.post with new title
            "type": "post",
            "title": new_title,
            "id": post_id,
            "page": self.post.page,
            "description": self.post.description,
            "contentType": self.post.contentType,
            "content": self.post.content,
            "author": AuthorSummarySerializer(self.post.author).data,
            "likes": likes,
            "published": self.post.published,
            "visibility": self.post.visibility
        }

        response = self.client.post(url, post_object, format='json')
        new_post = Post.objects.filter(fqid=post_id)
        self.assertTrue(new_post.exists())      # check for the id
        new_post = new_post.first()
        self.assertEqual(new_post.title, new_title)     # check that title was updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_resend_deleted_posts(self):
        url = reverse('api:authors:inbox', args=[self.author.id])
        post_id = self.post.fqid

        likes = LikesSerializer({
            'page': self.post.page,
            'id': self.post.fqid + "/likes",
            'page_number': 1,
            'size': 5,
            'count': 0,
            'src': [],
        }).data

        post_object = {     # post object version of self.post with visibility = "DELETED"
            "type": "post",
            "title": self.post.title,
            "id": post_id,
            "page": self.post.page,
            "description": self.post.description,
            "contentType": self.post.contentType,
            "content": self.post.content,
            "author": AuthorSummarySerializer(self.post.author).data,
            "likes": likes,
            "published": self.post.published,
            "visibility": "DELETED"
        }

        response = self.client.post(url, post_object, format='json')
        new_post = Post.objects.filter(fqid=post_id)
        self.assertTrue(new_post.exists())
        self.assertTrue(new_post.first().is_deleted)    # check that post is deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_public_images_with_remote(self):
        url = reverse('api:authors:inbox', args=[self.author.id])
        post_id = "http://nodebbbb/api/authors/222/posts/249"

        likes = LikesSerializer({
            'page': self.post.page,
            'id': self.post.fqid + "/likes",
            'page_number': 1,
            'size': 5,
            'count': 0,
            'src': [],
        }).data

        post_object = {
            "type": "post",
            "title": self.post.title,
            "id": post_id,
            "page": self.post.page,
            "description": self.post.description,
            "contentType": self.post.contentType,
            "content": "http://localhost:8000/media/images/test_image.png",
            "author": AuthorSummarySerializer(self.post.author).data,
            "likes": likes,
            "published": self.post.published,
            "visibility": "DELETED"
        }

        response = self.client.post(url, post_object, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)     # check that post was created
        new_post = Post.objects.filter(fqid=post_id)
        self.assertTrue(new_post.exists())
        
        new_post = new_post.first()
        image_response = self.client.get(new_post.content)
        self.assertEqual(image_response.status_code, status.HTTP_200_OK)    # check that image is public and visible

    
    def test_follow_remote_author(self):
        url = reverse('api:authors:inbox', args=[self.author.id])
        remote_author_id = "http://nodeaaaa/api/authors/111"
        
        follow_request_object = {
            "type": "follow",      
            "summary": f"Greg wants to follow {self.author.display_name}",
            "actor": {
                "type": "author",
                "id": remote_author_id,
                "host": "http://nodeaaaa/api/",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                "page": "http://nodeaaaa/authors/greg"
            },
            "object": AuthorSummarySerializer(self.author).data,
        }

        response = self.client.post(url, follow_request_object, format='json')
        new_remote_author_check = Author.objects.filter(fqid=remote_author_id)
        self.assertTrue(new_remote_author_check.exists())

        new_follow_request = Follow.objects.filter(user=self.author, follower=new_remote_author_check.first())
        self.assertTrue(new_follow_request.exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
