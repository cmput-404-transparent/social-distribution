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

    # get author info and update/edit author info by author id
    path("<int:author_id>/full/", author_views.get_full_author, name="get_full_author"),

    # get author info by fqid
    # path("<int:author_fqid>/",),      #################### NOT DONE YET ####################

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

    # FOLLOWING AND FRIENDS URLS ------------------------------------------------------------------------------

    # get follow requests
    path("<int:author_id>/follow_requests/", author_views.get_follow_requests, name="get_follow_requests"),

    # manage follow request
    path("<int:author_id>/follow_request/", author_views.manage_follow, name="manage_follow"),

    # get followers (GET method)
    path("<int:author_id>/followers/", author_views.followers, name="followers"),

    # get users that an author follows (GET method)     # unfollow (DELETE method)
    path("<int:author_id>/following/", author_views.following, name="following"),

    # get users that an author is friends with
    path("<int:author_id>/friends/", author_views.friends, name="friends"),

    # get relationship between two authors
    path("<int:author_1_id>/relationship/<int:author_2_id>/", author_views.get_relationship, name="get_relationship"),

    # POSTS URLS ------------------------------------------------------------------------------

    # Get recent posts from author              # Create a new post (POST method)
    path('<int:author_id>/posts/', posts_views.author_posts, name='author_posts'),

    # Retrieve a specific post           # Update an existing post (PUT method)               # Delete a post (DELETE method)       
    path('<int:author_id>/posts/<uuid:post_id>/', posts_views.post_detail, name='get_post'),

    # VISIBILITY URLS ------------------------------------------------------------------------------

    # get all stream posts for a user
    path('<int:author_id>/stream/', posts_views.stream, name='stream'),

    # SHARING URLS ------------------------------------------------------------------------------

    # share post
    path('<uuid:post_id>/share/', posts_views.share_post, name='share_post'),

    # get shared posts
    path('<str:author_id>/shared_posts/', posts_views.list_shared_posts, name='list_shared_posts'),

    # IMAGE URLS ------------------------------------------------------------------------------

    path('<int:author_id>/posts/<uuid:post_id>/image/', posts_views.get_image_post, name='get_image_post'),

    path('upload_image/', posts_views.upload_image, name='upload_image'),

    # Admin-only ------------------------------------------------------------------------------

    path('create/', author_views.create_author, name='create_author'),
    path('<int:author_id>/modify/', author_views.modify_author, name='modify_author'),
    path('<int:author_id>/delete/', author_views.delete_author, name='delete_author'),
]
