
from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    # # Get recent posts from author
    # path('authors/<int:author_id>/posts/', views.list_author_posts,name='list_author_posts'),
    
    # # Create a new post (POST method)
    # path('authors/<int:author_id>/posts/create/', views.create_new_post, name='create_new_post'),
    
    # # Retrieve a specific post
    # path('authors/<int:author_id>/posts/<int:post_id>/', views.get_post, name='get_post'),
    
    # # Update an existing post (PUT method)
    # path('authors/<int:author_id>/posts/<int:post_id>/edit/', views.update_existing_post, name='update_existing_post'),
    

    # # Delete a post (DELETE method)
    # path('authors/<int:author_id>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),



    # path('<int:author_id>/posts/', views.list_author_posts, name='list_author_posts'),
    # path('<int:author_id>/posts/create/', views.create_new_post, name='create_new_post'),


    path('<int:author_id>/posts/', views.author_posts, name='author_posts'),


    # Retrieve a specific post           # Update an existing post (PUT method)               # Delete a post (DELETE method)       
    path('<int:author_id>/posts/<int:post_id>/', views.post_detail, name='get_post'),
    

    path('authors/<int:author_id>/add_friend/', views.add_friend, name='add_friend'),
    path('authors/<int:author_id>/remove_friend/', views.remove_friend, name='remove_friend'),


    # get all public posts on node
    path('public/', views.get_all_public_posts, name='get_public'),

    path('<int:post_id>/share/', views.share_post, name='share_post'),
    path('authors/<str:author_id>/shared_posts/', views.list_shared_posts, name='list_shared_posts'),
]
