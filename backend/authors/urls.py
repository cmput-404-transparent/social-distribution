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

    # POSTS URLS ------------------------------------------------------------------------------

    # Get recent posts from author
    path('<int:author_id>/posts/', posts_views.author_posts, name='author_posts'),

    # Create a new post (POST method)
    path('<int:author_id>/posts/create/', posts_views.create_new_post, name='create_new_post'),

    # Retrieve a specific post           # Update an existing post (PUT method)               # Delete a post (DELETE method)       
    path('<int:author_id>/posts/<int:post_id>/', posts_views.post_detail, name='get_post'),

    # Update an existing post (PUT method)
    path('<int:author_id>/posts/<int:post_id>/edit/', posts_views.update_existing_post, name='update_existing_post'),

    # Delete a post (DELETE method)
    path('<int:author_id>/posts/<int:post_id>/delete/', posts_views.delete_post, name='delete_post'),
    
    # add friend
    path('<int:author_id>/add_friend/', posts_views.add_friend, name='add_friend'),

    # remove friend
    path('<int:author_id>/remove_friend/', posts_views.remove_friend, name='remove_friend'),

    # get all public posts on node
    path('posts/public/', posts_views.get_all_public_posts, name='get_public'),

    # share post
    path('<int:post_id>/share/', posts_views.share_post, name='share_post'),

    # get shared posts
    path('<str:author_id>/shared_posts/', posts_views.list_shared_posts, name='list_shared_posts'),
]
