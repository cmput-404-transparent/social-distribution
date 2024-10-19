from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("authors/", include("authors.urls")),
    path('authors/', include('posts.urls')),

    # path("authors/", include("posts.urls")), 
]
