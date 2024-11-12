import uuid
from django.db import models
from django.conf import settings

# Create your models here.
# Model representing a post
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for the post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Author of the post
    title = models.CharField(max_length=100)  # Title of the post
    page = models.CharField(max_length=300)     # Page of the post
    content = models.TextField()  # Content of the post
    description = models.TextField(blank=True)  # Optional description of the post
    contentType = models.CharField(choices=CONTENT_TYPE_CHOICES, max_length=20, default='text/plain')  # Type of content
    published = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was published
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')  # Visibility of the post
    is_shared = models.BooleanField(default=False)  # Indicates if the post is shared
    original_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='shares')  # Reference to the original post if shared
    shares_count = models.PositiveIntegerField(default=0)  # Count of shares
    github_activity_id = models.IntegerField(blank=True, null=True)  # GitHub activity ID
    is_deleted = models.BooleanField(default=False)  # Indicates if the post is deleted
    fqid = models.CharField(unique=True, max_length=200, blank=True, null=True)  # Fully qualified ID

    def save(self, *args, **kwargs):
        # Override save method to set fqid and page if not already set
        if not self.fqid:
            self.fqid = f"{self.author.host}authors/{self.author.id}/posts/{self.id}"
        if not self.page:
            self.page = f"{self.author.page}/posts/{self.id}"
        super().save(*args, **kwargs)

    @property
    def is_shareable(self):
        # Property to check if the post is shareable
        return self.visibility == 'PUBLIC'

    def increment_shares_count(self):
        # Method to increment the shares count
        self.shares_count += 1
        self.save()

    def __str__(self):
        # String representation of the post
        return self.title

# Model representing a share of a post
class Share(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for the share
    sharer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shares')  # User who shared the post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared_by')  # Post that was shared
    shared_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was shared

    class Meta:
        unique_together = ['sharer', 'post']  # Ensures a user can share a post only once

    def __str__(self):
        # String representation of the share
        return f"{self.sharer.username} shared {self.post.title}"

# Model representing a like on a post or comment
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for the like
    type = models.CharField(default='like', max_length=10)  # Type of like
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User who liked the post or comment
    object = models.CharField(max_length=200)  # URL of the liked object
    published = models.DateTimeField(auto_now_add=True)  # Timestamp when the like was made
    fqid = models.URLField(blank=True, null=True)

    def __str__(self):
        # String representation of the like
        return f"{self.author} liked {self.object}"
    
    def save(self, *args, **kwargs):
        # Override save method to set fqid
        try:
            comment = Comment.objects.get(fqid=self.object)
            if not self.fqid:
                self.fqid = f"{comment.post.author.host}authors/{self.author.id}/liked/{self.id}"
        except:
            post = Post.objects.get(fqid=self.object)
            if not self.fqid:
                self.fqid = f"{post.author.host}authors/{self.author.id}/liked/{self.id}"
        super().save(*args, **kwargs)

# Model representing a comment on a post
class Comment(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text/plain', 'Plain Text'),
        ('text/markdown', 'Markdown'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for the comment
    type = models.CharField(default='comment', max_length=10)  # Type of comment
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User who made the comment
    comment = models.TextField()  # Content of the comment
    contentType = models.CharField(choices=CONTENT_TYPE_CHOICES, max_length=50, default='text/plain')  # Type of content
    published = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment was made
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Post that was commented on
    fqid = models.CharField(unique=True, max_length=200, blank=True, null=True)  # Fully qualified ID

    def save(self, *args, **kwargs):
        # Override save method to set fqid if not already set
        if not self.fqid:
            self.fqid = f"{self.author.host}authors/{self.author.id}/commented/{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        # String representation of the comment
        return f"Comment by {self.author} on {self.post.title}"
