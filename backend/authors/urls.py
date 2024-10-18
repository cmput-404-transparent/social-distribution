from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    # get author info by author id
    path("<int:author_id>/", views.get_author, name="get_author"),
    # edit author by author id
    path("<int:author_id>/edit/", views.edit_author, name="edit_author"),
    # login
    path("login/", views.login, name="login"),
    # signup
    path("signup/", views.signup, name="signup"),
    # get author info from session cookie
    path("get/from_session/", views.get_author_from_session, name="get_author_from_session")
]
