
from django.urls import path , re_path
from . import views

app_name = "posts"

urlpatterns = [
    # Get recent posts from author
    path('authors/<int:author_id>/posts/', views.list_author_posts,name='list_author_posts'),
    
    # Create a new post (POST method)
    path('authors/<int:author_id>/posts/create/', views.create_new_post, name='create_new_post'),
    
    # Retrieve a specific post
    path('authors/<int:author_id>/posts/<int:post_id>/', views.get_post, name='get_post'),
    
    # Update an existing post (PUT method)
    path('authors/<int:author_id>/posts/<int:post_id>/edit/', views.update_existing_post, name='update_existing_post'),
    
    # Delete a post (DELETE method)
    path('authors/<int:author_id>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    # Comment API
    path('authors/<str:author_serial>/commented', views.author_commented),
    path('authors/<str:author_serial>/commented/<str:comment_serial>', views.get_comment_by_serial),
    re_path(r'^commented/(?P<comment_fqid>.+)$', views.get_comment_by_fqid),
    re_path(r'^authors/(?P<author_fqid>.+)/commented$', views.author_fqid_commented),
    # Likes API
    path('authors/<str:author_serial>/inbox', views.send_like_to_inbox),
    path('authors/<str:author_serial>/posts/<str:post_serial>/likes', views.get_post_likes),
    path('posts/<str:post_fqid>/likes', views.get_post_likes_by_fqid),
    path('authors/<str:author_serial>/posts/<str:post_serial>/comments/<str:comment_serial>/likes', views.get_comment_likes),
    path('liked/<str:like_fqid>', views.get_like_by_fqid),

    # Liked API
    path('authors/<str:author_serial>/liked', views.get_liked_by_author),
    path('authors/<str:author_serial>/liked/<str:like_serial>', views.get_single_like_by_author),
    path('authors/<str:author_fqid>/liked', views.get_liked_by_author_fqid),
    path('liked/<str:like_fqid>', views.get_like_by_fqid_local),
]
