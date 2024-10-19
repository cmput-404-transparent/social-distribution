
from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [

    # Get recent posts from author
    path('<int:author_id>/posts/', views.author_posts, name='author_posts'),

    # Create a new post (POST method)
    path('<int:author_id>/posts/create/', views.create_new_post, name='create_new_post'),

    # Retrieve a specific post           # Update an existing post (PUT method)               # Delete a post (DELETE method)       
    path('<int:author_id>/posts/<int:post_id>/', views.post_detail, name='get_post'),

    # Update an existing post (PUT method)
    path('<int:author_id>/posts/<int:post_id>/edit/', views.update_existing_post, name='update_existing_post'),

    # Delete a post (DELETE method)
    path('<int:author_id>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    # add friend
    path('authors/<int:author_id>/add_friend/', views.add_friend, name='add_friend'),

    # remove friend
    path('authors/<int:author_id>/remove_friend/', views.remove_friend, name='remove_friend'),

    # get all public posts on node
    path('public/', views.get_all_public_posts, name='get_public'),

    # share post
    path('<int:post_id>/share/', views.share_post, name='share_post'),

    # get shared posts
    path('authors/<str:author_id>/shared_posts/', views.list_shared_posts, name='list_shared_posts'),


    path('<int:author_id>/stream/', views.stream, name='stream'),
]
