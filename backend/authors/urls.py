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

    # author inbox
    path("<int:author_id>/inbox/", author_views.inbox, name="inbox"),

    # get author info and update/edit author info by author id
    path("<int:author_id>/full/", author_views.get_full_author, name="get_full_author"),

    # get author info by fqid
    # path("<int:author_fqid>/",),      #################### NOT DONE YET ####################

    # login
    path("login/", author_views.login, name="login"),

    # signup
    path("signup/", author_views.signup, name="signup"),

    # logout
    path("logout/", author_views.logout, name="logout"),

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

    # IMAGE URLS ------------------------------------------------------------------------------

    path('<int:author_id>/posts/<uuid:post_id>/image/', posts_views.get_image_post, name='get_image_post'),

    path('upload_image/', posts_views.upload_image, name='upload_image'),

    path('images/all/', posts_views.get_all_hosted_images, name="get_all_images"),

    # LIKES URLS ------------------------------------------------------------------------------

    # Get likes for a specific object
    path('<int:author_id>/posts/<uuid:object_id>/likes', posts_views.get_likes),
    
    # Like a specific object
    path('<int:author_id>/posts/<uuid:object_id>/like', posts_views.like_object),

    # check if an author liked a post
    path('<int:author_id>/liked/<uuid:post_id>', posts_views.check_liked),

    # COMMENTS URLS ------------------------------------------------------------------------------
    
    # Comments API
    # Get comments on a specific post
    path('<int:author_serial>/posts/<uuid:post_serial>/comments', posts_views.comments_on_post),
    
    # Get a specific comment on a post
    path('<int:author_serial>/posts/<uuid:post_serial>/comments/<uuid:comment_id>', posts_views.get_comment),

    # Get likes for a specific comment on a post
    path('<int:author_serial>/posts/<uuid:post_serial>/comments/<path:comment_fqid>/likes', posts_views.get_comment_likes),
    
    # Commented API
    # Get comments made by a specific author
    path('<int:author_serial>/commented', posts_views.get_author_comments),
    
    # Get a specific comment made by a specific author
    path('<int:author_serial>/commented/<uuid:comment_serial>', posts_views.get_author_comment),

    # remote nodes
    path('remote-nodes/', author_views.manage_remote_nodes, name='manage_remote_nodes'),

    # BY FQID URLS ------------------------------------------------------------------------------

    # get author comments by author fqid
    path("<path:author_fqid>/commented/", posts_views.get_author_comments_by_fqid, name="get_author_comments_by_fqid"),

    # get author comments by author fqid
    path("<path:author_fqid>/likes/", posts_views.get_author_likes_by_fqid, name="get_author_likes_by_fqid"),

    # get author by fqid
    path("<path:author_fqid>/", author_views.get_author_by_fqid, name="get_author_by_fqid"),

]
