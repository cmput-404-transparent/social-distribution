from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    # Get a specific post by its fqid
    path("<path:post_fqid>/", views.get_post, name="get_post"),
    
    # Post GitHub activity for a specific author
    path('<int:author_id>/github/', views.post_github_activity, name="post_github"),
    
    # Get an image post by its fqid
    path("<str:fqid>/image/", views.get_image_post_by_fqid, name="get_image_post_by_fqid")
]
