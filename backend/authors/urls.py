from django.urls import path
from . import author_views
from . import posts_views

app_name = "authors"

urlpatterns = [
    
    # AUTHOR URLS ------------------------------------------------------------------------------

    # get author info by author id
    path("<int:author_id>/", author_views.get_author, name="get_author"),

    # edit author by author id
    path("<int:author_id>/edit/", author_views.edit_author, name="edit_author"),

    # login
    path("login/", author_views.login, name="login"),

    # signup
    path("signup/", author_views.signup, name="signup"),

    # get author info from session cookie
    path("get/from_session/", author_views.get_author_from_session, name="get_author_from_session"),

    # search authors
    path("search/", author_views.search_author, name="search_author"),

    # follow author
    path("follow/", author_views.follow, name="follow"),

    # get follow requests
    path("<int:author_id>/follow_requests/", author_views.get_follow_requests, name="get_follow_requests"),

    # manage follow request
    path("<int:author_id>/follow_request/", author_views.manage_follow, name="manage_follow"),

    # get followers
    path("<int:author_id>/followers/", author_views.get_followers, name="get_followers"),

    # get users that an author follows
    path("<int:author_id>/following/", author_views.get_following, name="get_following"),

    # POSTS URLS ------------------------------------------------------------------------------

    # Get recent posts from author
    path('<int:author_id>/posts/', posts_views.author_posts, name='author_posts'),

    # Create a new post (POST method)
    path('<int:author_id>/posts/create/', posts_views.create_new_post, name='create_new_post'),

    # Retrieve a specific post           # Update an existing post (PUT method)               # Delete a post (DELETE method)       
    path('<int:author_id>/posts/<int:post_id>/', posts_views.post_detail, name='get_post'),

    # VISIBILITY URLS ------------------------------------------------------------------------------

    # get all public posts on node
    path('posts/public/', posts_views.get_all_public_posts, name='get_public'),

    # get all stream posts for a user
    path('<int:author_id>/stream/', posts_views.stream, name='stream'),

    # SHARING URLS ------------------------------------------------------------------------------

    # share post
    path('<int:post_id>/share/', posts_views.share_post, name='share_post'),

    # get shared posts
    path('<str:author_id>/shared_posts/', posts_views.list_shared_posts, name='list_shared_posts'),
]
