
from django.urls import path
from . import views

app_name = "commented"

urlpatterns = [
    path('<path:comment_fqid>/', views.get_comment_by_fqid, name="get_comment_by_fqid"),
]
