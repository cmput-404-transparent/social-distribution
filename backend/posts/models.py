from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    host = models.URLField()
    display_name = models.CharField(max_length=100)
    github = models.URLField(blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    page = models.URLField()

    def is_friend(self, user):
        return Friend.objects.filter(user=self.user, friend=user).exists()

    def __str__(self):
        return self.display_name

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'friend']

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('UNLISTED', 'Unlisted'),
        ('FRIENDS', 'Friends Only'),
    ]

    CONTENT_TYPE_CHOICES = [
        ('text/plain', 'Plain Text'),
        ('text/markdown', 'Markdown'),
        ('image/png;base64', 'PNG Image'),
        ('image/jpeg;base64', 'JPEG Image'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField(blank=True)
    contentType = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='text/plain')
    published = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')

    def __str__(self):
        return self.title