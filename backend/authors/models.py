'''
source: ChatGPT (OpenAI)
prompt: "i know django has built in user authentication with an object called User, but my User
        in my app is called Author. how do i make it so i can use django's authentication framework with Author?"
date: October 15, 2024
'''

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class AuthorManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        extra_fields.setdefault('is_active', True)
        author = self.model(username=username, **extra_fields)
        author.set_password(password)  # Password hashing
        author.save(using=self._db)
        return author

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)


class Author(AbstractBaseUser, PermissionsMixin):
    host = models.URLField()
    display_name = models.CharField(max_length=100)
    github = models.URLField(blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    page = models.URLField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AuthorManager()

    USERNAME_FIELD = 'username'

class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField(blank=True)
    contentType = models.CharField(choices=CONTENT_TYPE_CHOICES, max_length=20, default= 'text/plain')
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')
    is_shared = models.BooleanField(default=False)
    original_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='shares')
    shares_count = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    @property
    def is_shareable(self):
        return self.visibility == 'PUBLIC'

    def increment_shares_count(self):
        self.shares_count += 1
        self.save()

    def __str__(self):
        return self.title

class Share(models.Model):
    sharer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared_by')
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['sharer', 'post']

    def __str__(self):
        return f"{self.sharer.username} shared {self.post.title}"
