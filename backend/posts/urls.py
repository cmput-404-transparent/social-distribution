from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("<int:fqid>/", views.get_post, name="get_post"),
    path('<int:author_id>/github/', views.post_github_activity, name="post_github"),
    path("<int:fqid>/image/", views.get_image_post_by_fqid, name="get_image_post_by_fqid")
]
