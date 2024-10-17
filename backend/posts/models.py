
from django.db import models
from django.utils import timezone
from authors.models import Author
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('FRIENDS', 'Friends Only'),
        ('UNLISTED', 'Unlisted'),
        ('DELETED', 'Deleted'),
    ]

    CONTENT_TYPE_CHOICES = [
        ('text/plain', 'Plain Text'),
        ('text/markdown', 'Markdown'),
        ('image/png;base64', 'PNG Image'),
        ('image/jpeg;base64', 'JPEG Image'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    source = models.URLField()
    origin = models.URLField()
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')
    unlisted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    content_type = models.CharField(max_length=50, default='text/plain')
    published = models.DateTimeField(default=timezone.now)

    def get_fqid(self):
        return f"{self.author.host}posts/{self.id}/"
    
    def get_page_url(self):
        return f"{self.author.host}authors/{self.author.username}/posts/{self.id}/"
    
    def get_fqid(self):
        return f"{self.author.host}authors/{self.author.id}/commented/{self.id}/"
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    context = models.URLField()
    summary = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.URLField()  # URL to the liked object (Post or Comment)

    def __str__(self):
        return f'Like by {self.author} on {self.object}'
