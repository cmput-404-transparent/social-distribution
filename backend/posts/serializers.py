from rest_framework import serializers
from .models import *
import commonmark
from django.core.files.base import ContentFile
import base64
from authors.serializers import AuthorSummarySerializer
# Serializer for Post model
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.CharField(default='post', read_only=True)

    class Meta:
        model = Post
        fields = ['type', 'id', 'title', 'description', 'contentType', 'content', 'author', 'published', 'visibility', 'is_shared', 'original_post', 'shares_count']
        read_only_fields = ['type', 'id', 'author', 'published', 'is_shared', 'original_post', 'shares_count']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove fields based on whether the post is shared or not
        if instance.is_shared:
            representation.pop('shares_count', None)
        else:
            representation.pop('is_shared', None)
            representation.pop('original_post', None)
        return representation

    def validate(self, data):
        # Validate base64 content for images
        if data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            try:
                base64.b64decode(data['content'])
            except Exception:
                raise serializers.ValidationError("Invalid base64 content for image.")
        return data

    def create(self, validated_data):
        # Handle content based on contentType
        if validated_data.get('contentType') == 'text/markdown':
            validated_data['content'] = self.render_commonmark(validated_data['content'])
        elif validated_data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')
            ext = format.split('/')[-1]
            validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"post_image_{validated_data['id']}.{ext}")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle content based on contentType
        if validated_data.get('contentType') == 'text/markdown':
            validated_data['content'] = self.render_commonmark(validated_data['content'])
        elif validated_data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')
            ext = format.split('/')[-1]
            validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"post_image_{instance.id}.{ext}")
        return super().update(instance, validated_data)

    @staticmethod
    def render_commonmark(text):
        # Render markdown content to HTML
        parser = commonmark.Parser()
        renderer = commonmark.HtmlRenderer()
        ast = parser.parse(text)
        return renderer.render(ast)

# Serializer for Share model
class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['id', 'sharer', 'post', 'shared_at']
        read_only_fields = ['id', 'sharer', 'shared_at']

# Serializer for summarizing Post model
class PostSummarySerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='post', read_only=True)
    id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_id(self, obj):
        return f"{obj.author.host}authors/{obj.author.id}/posts/{obj.id}"
    
    def get_likes_count(self, obj):
        return Like.objects.filter(object=obj.get_absolute_url()).count()

    class Meta:
        model = Post
        fields = [
            'type', 'title', 'id', 'description', 'contentType', 'content',
            'author', 'published', 'visibility', 'likes_count'
        ]

# Serializer for Like model
class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='like', read_only=True)
    author = AuthorSummarySerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['type', 'author', 'published', 'id', 'object']

# Serializer for a list of likes
class LikesSerializer(serializers.Serializer):
    type = serializers.CharField(default='likes', read_only=True)
    page = serializers.CharField()
    id = serializers.CharField()
    page_number = serializers.IntegerField()
    size = serializers.IntegerField()
    count = serializers.IntegerField()
    src = LikeSerializer(many=True)

# Serializer for Comment model
class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='comment', read_only=True)
    author = AuthorSummarySerializer(read_only=True)
    id = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    page = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    published = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'contentType', 'published', 'id', 'post', 'page', 'likes']

    def get_id(self, obj):
        return f"{obj.author.host}api/authors/{obj.author.id}/commented/{obj.id}"

    def get_post(self, obj):
        return f"{obj.post.author.host}api/authors/{obj.post.author.id}/posts/{obj.post.id}"

    def get_page(self, obj):
        # URL to view the comment in HTML (if available)
        return f"{obj.post.author.host}authors/{obj.post.author.id}/posts/{obj.post.id}"

    def get_likes(self, obj):
        likes = Like.objects.filter(object=self.get_id(obj))
        likes_serializer = LikesSerializer({
            'page': f"{obj.author.host}authors/{obj.author.id}/commented/{obj.id}/likes",
            'id': f"{obj.author.host}api/authors/{obj.author.id}/commented/{obj.id}/likes",
            'page_number': 1,
            'size': 50,
            'count': likes.count(),
            'src': likes[:50],  # Return first 50 likes
        })
        return likes_serializer.data

# Serializer for a list of comments
class CommentsSerializer(serializers.Serializer):
    type = serializers.CharField(default='comments', read_only=True)
    page = serializers.CharField()
    id = serializers.CharField()
    page_number = serializers.IntegerField()
    size = serializers.IntegerField()
    count = serializers.IntegerField()
    src = CommentSerializer(many=True)
