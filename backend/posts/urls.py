
from django.urls import path
from . import views

urlpatterns = [

    # Get recent posts from author
    path('authors/<int:author_id>/posts/', views.list_recent_posts, name='list_recent_posts'),
    
    # Create a new post (POST method)
    path('authors/<int:author_id>/posts/create/', views.create_post, name='create_post'),
    
    # Retrieve a specific post
    path('authors/<int:author_id>/posts/<int:post_id>/', views.get_post, name='get_post'),
    
    # Update an existing post (PUT method)
    path('authors/<int:author_id>/posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    
    # Delete a post (DELETE method)
    path('authors/<int:author_id>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]
