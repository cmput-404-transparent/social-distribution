from django.urls import path
from . import author_views
from . import posts_views

app_name = "authors"

urlpatterns = [
    # AUTHOR URLS ------------------------------------------------------------------------------

    # get all authors
    path("", author_views.get_all_authors, name="get_all_authors"),

    # get author info and update/edit author info by author id
    path("<int:author_id>/", author_views.get_update_author, name="get_update_author"),

    # login
    path("login/", author_views.login, name="login"),

    # signup
    path("signup/", author_views.signup, name="signup"),

    # get author info from session cookie
    path("get/from_session/", author_views.get_author_from_session, name="get_author_from_session"),

    # search authors
    path("search/", author_views.search_author, name="search_author"),

    # POSTS URLS ------------------------------------------------------------------------------

    # Get recent posts from author              # Create a new post (POST method)
    path('<int:author_id>/posts/', posts_views.author_posts, name='author_posts'),

    # Retrieve a specific post           # Update an existing post (PUT method)               # Delete a post (DELETE method)       
    path('<int:author_id>/posts/<int:post_id>/', posts_views.post_detail, name='get_post'),

    # VISIBILITY URLS ------------------------------------------------------------------------------

    # add friend
    path('<int:author_id>/add_friend/', posts_views.add_friend, name='add_friend'),

    # remove friend
    path('<int:author_id>/remove_friend/', posts_views.remove_friend, name='remove_friend'),

    # get all public posts on node
    path('posts/public/', posts_views.get_all_public_posts, name='get_public'),

    # get all stream posts for a user
    path('<int:author_id>/stream/', posts_views.stream, name='stream'),

    # SHARING URLS ------------------------------------------------------------------------------

    # share post
    path('<int:post_id>/share/', posts_views.share_post, name='share_post'),

    # get shared posts
    path('<str:author_id>/shared_posts/', posts_views.list_shared_posts, name='list_shared_posts'),

    # IMAGE URLS ------------------------------------------------------------------------------

    path('<int:author_id>/posts/<int:post_id>/image/', posts_views.get_image_post, name='get_image_post'),
]
