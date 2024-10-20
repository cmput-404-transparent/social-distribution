from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("<int:fqid>/", views.get_post, name="get_post"),
    path('<int:author_id>/github/', views.post_github_activity, name="post_github")
]
