from django.db import models
from django.conf import settings

# Create your models here.

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
    github_activity_id = models.IntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    fqid = models.CharField(unique=True, max_length=200, blank=True, null=True)

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
