from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("<int:fqid>/", views.get_post, name="get_post"),
    path('<int:author_id>/github/', views.post_github_activity, name="post_github"),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/likes', views.get_likes),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/like', views.like_object),
    path("<int:fqid>/image/", views.get_image_post_by_fqid, name="get_image_post_by_fqid")
]
