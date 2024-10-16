from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path("<int:author_id>/", views.get_author, name="get_author"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("get/from_session/", views.get_author_from_session, name="get_author_from_session")
]