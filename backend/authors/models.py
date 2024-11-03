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

        author = self.create_user(username, password, **extra_fields)

        # Automatically set the host and page fields
        author.host = f"http://localhost:3000/api/"
        author.page = f"{author.host}/authors/{author.id}"
        author.github = "http://github.com/"
        author.save(using=self._db)

        return author


class Author(AbstractBaseUser, PermissionsMixin):
    host = models.URLField(blank=True, null=True)
    display_name = models.CharField(max_length=100)
    github = models.URLField(blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    page = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AuthorManager()

    USERNAME_FIELD = 'username'

class Follow(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('FOLLOWED', 'Followed')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default= 'REQUESTED')

    class Meta:
        unique_together = ['user', 'follower']

    @staticmethod
    def are_friends(user1, user2):
        follow_1 = Follow.objects.filter(user=user1, follower=user2, status='FOLLOWED').exists()
        follow_2 = Follow.objects.filter(user=user2, follower=user1, status='FOLLOWED').exists()
        return follow_1 and follow_2

    @staticmethod
    def get_friends(user):
        friends_1 = Follow.objects.filter(user=user, status='FOLLOWED').values_list('follower')
        friends_2 = Follow.objects.filter(follower=user, status='FOLLOWED').values_list('user')
        return friends_1.intersection(friends_2)



# class RemoteNode(models.Model):
#     url = models.URLField(unique=True)  # the URL of the remote node
#     username = models.CharField(max_length=200)  
#     password = models.CharField(max_length=250)  
#     created_at = models.DateTimeField(auto_now_add=True)


class RemoteNode(models.Model):
    url = models.URLField(unique=True)
    username = models.CharField(max_length=250)
    token = models.CharField(max_length=250, blank=True, null=True) 


