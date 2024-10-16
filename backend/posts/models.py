
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
