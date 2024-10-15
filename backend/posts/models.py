# from django.db import models
# from django.contrib.auth.models import User

# class Post(models.Model):
#     VISIBILITY_CHOICES = [
#         ('PUBLIC', 'Public'),
#         ('FRIENDS', 'Friends'),
#         ('UNLISTED', 'Unlisted'),
#         ('DELETED', 'Deleted')
#     ]
#     # Fields for Post
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     content_type = models.CharField(max_length=100)
#     content = models.TextField()
#     visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)
#     published = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

#     def __str__(self):
#         return self.title



# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Post(models.Model):
#     CONTENT_TYPE_CHOICES = [
#         ('text/markdown', 'Markdown'),
#         ('text/plain', 'Plain Text'),
#         ('image/png;base64', 'PNG Image (base64)'),
#         ('image/jpeg;base64', 'JPEG Image (base64)'),
#     ]
    
#     VISIBILITY_CHOICES = [
#         ('PUBLIC', 'Public'),
#         ('FRIENDS', 'Friends'),
#         ('UNLISTED', 'Unlisted'),
#         ('DELETED', 'Deleted'),
#     ]
    
#     id = models.AutoField(primary_key=True)  # Auto-generated ID for the post
#     author = models.ForeignKey(User, on_delete=models.CASCADE)  # link to the author
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     contentType = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES, default='text/plain')
#     content = models.TextField()
#     published = models.DateTimeField(auto_now_add=True)
#     visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')

#     def __str__(self):
#         return self.title


from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text/plain', 'Plain Text'),
        ('text/markdown', 'Markdown'),
        ('image/png;base64', 'PNG Image'),
        ('image/jpeg;base64', 'JPEG Image'),
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    contentType = models.CharField(choices=CONTENT_TYPE_CHOICES, max_length=20, default= 'text/plain')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
