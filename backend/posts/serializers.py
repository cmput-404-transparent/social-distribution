from rest_framework import serializers
from .models import Post, Comment, Like
from backend.authors.serializers import AuthorSerializer, AuthorSummarySerializer
import base64
from django.core.files.base import ContentFile


class PostSerializer(serializers.ModelSerializer):
    contentType = serializers.CharField(source='content_type')
    author = AuthorSerializer()  # Replace with your actual AuthorSerializer
    visibility = serializers.CharField(source='get_visibility_display')

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'contentType', 'content',
            'author', 'published', 'visibility', 'unlisted'
        ]

    def validate(self, data):
        content_type = data.get('content_type')
        if content_type in ['image/png;base64', 'image/jpeg;base64']:
            content = data.get('content')
            if ';base64,' in content:
                header, base64_data = content.split(';base64,')
            else:
                base64_data = content
            try:
                base64.b64decode(base64_data)
            except Exception:
                raise serializers.ValidationError({
                    "content": "Invalid base64 content for image."
                })
        return data
        # def create(self, validated_data):
        #     if validated_data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
        #         # Handle base64 image
        #         format, imgstr = validated_data['content'].split(';base64,')  # Split base64 string
        #         ext = format.split('/')[-1]  # Get extension (png or jpeg)
        #         validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        #     return super().create(validated_data)

        # def update(self, instance, validated_data):
        #     if validated_data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
        #         format, imgstr = validated_data['content'].split(';base64,')
        #         ext = format.split('/')[-1]
        #         validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        #     return super().update(instance, validated_data)




class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='comment', read_only=True)
    author = AuthorSerializer()
    contentType = serializers.CharField(source='content_type')
    id = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    page = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'contentType', 'published', 'id', 'post', 'page']

    def get_id(self, obj):
        return f"{obj.author.host}authors/{obj.author.id}/commented/{obj.id}/"

    def get_post(self, obj):
        return obj.post.get_fqid()

    def get_page(self, obj):
        # This could be the post's page or a specific comment page
        return obj.post.get_page_url()


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='Like', read_only=True)
    author = AuthorSummarySerializer()
    object = serializers.URLField()

    class Meta:
        model = Like
        fields = ['type', 'summary', 'author', 'object']