from django.urls import path
from . import views

app_name = "liked"

urlpatterns = [
    path('<path:like_fqid>/', views.get_like_by_fqid, name="get_like_by_fqid"),
]
