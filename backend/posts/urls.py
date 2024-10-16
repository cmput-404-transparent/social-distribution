from django.urls import path
from . import views

urlpatterns = [
    path('authors/<int:author_id>/posts/', views.list_author_posts, name='list_author_posts'),
    path('authors/<int:author_id>/posts/create/', views.create_new_post, name='create_new_post'),
    path('authors/<int:author_id>/posts/<int:post_id>/', views.get_post, name='get_post'),
    path('authors/<int:author_id>/posts/<int:post_id>/update/', views.update_existing_post, name='update_existing_post'),
    path('authors/<int:author_id>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('authors/<int:author_id>/add_friend/', views.add_friend, name='add_friend'),
    path('authors/<int:author_id>/remove_friend/', views.remove_friend, name='remove_friend'),
]