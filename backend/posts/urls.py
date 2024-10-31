from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    # Get a specific post by its fqid
    path("<int:fqid>/", views.get_post, name="get_post"),
    
    # Post GitHub activity for a specific author
    path('<int:author_id>/github/', views.post_github_activity, name="post_github"),
    
    # Get likes for a specific post
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/likes', views.get_likes),
    
    # Like a specific post
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/like', views.like_object),
    
    # Comments API
    # Get comments on a specific post
    path('authors/<uuid:author_serial>/posts/<uuid:post_serial>/comments', views.comments_on_post),
    
    # Get a specific comment on a post
    path('authors/<uuid:author_serial>/posts/<uuid:post_serial>/comments/<uuid:comment_id>', views.get_comment),
    
    # Commented API
    # Get comments made by a specific author
    path('authors/<uuid:author_serial>/commented', views.get_author_comments),
    
    # Get a specific comment made by a specific author
    path('authors/<uuid:author_serial>/commented/<uuid:comment_serial>', views.get_author_comment),
    
    # Get an image post by its fqid
    path("<int:fqid>/image/", views.get_image_post_by_fqid, name="get_image_post_by_fqid")
]
