'''
source: ChatGPT (OpenAI)
prompt: "i know django has built in user authentication with an object called User, but my User
        in my app is called Author. how do i make it so i can use django's authentication framework with Author?"
date: October 15, 2024
'''

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

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
