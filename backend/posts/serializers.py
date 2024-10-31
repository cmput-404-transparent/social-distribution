from rest_framework import serializers
from .models import *
import commonmark
from django.core.files.base import ContentFile
import base64
from authors.serializers import AuthorSummarySerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.CharField(default='post', read_only=True)
    class Meta:
        model = Post
        fields = ['type', 'id', 'title', 'description', 'contentType', 'content', 'author', 'published', 'visibility', 'is_shared', 'original_post', 'shares_count']
        read_only_fields = ['type', 'id', 'author', 'published', 'is_shared', 'original_post', 'shares_count']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_shared:
            representation.pop('shares_count', None)
        else:
            representation.pop('is_shared', None)
            representation.pop('original_post', None)
        return representation

    def validate(self, data):
        if data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            try:
                base64.b64decode(data['content'])
            except Exception:
                raise serializers.ValidationError("Invalid base64 content for image.")
        return data

    def create(self, validated_data):
        if validated_data.get('contentType') == 'text/markdown':
            validated_data['content'] = self.render_commonmark(validated_data['content'])
        elif validated_data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')
            ext = format.split('/')[-1]
            validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"post_image_{validated_data['id']}.{ext}")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('contentType') == 'text/markdown':
            validated_data['content'] = self.render_commonmark(validated_data['content'])
        elif validated_data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')
            ext = format.split('/')[-1]
            validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"post_image_{instance.id}.{ext}")
        return super().update(instance, validated_data)

    @staticmethod
    def render_commonmark(text):
        parser = commonmark.Parser()
        renderer = commonmark.HtmlRenderer()
        ast = parser.parse(text)
        return renderer.render(ast)

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['id', 'sharer', 'post', 'shared_at']
        read_only_fields = ['id', 'sharer', 'shared_at']

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


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='like', read_only=True)
    author = AuthorSummarySerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['type', 'author', 'published', 'id', 'object']

class LikesSerializer(serializers.Serializer):
    type = serializers.CharField(default='likes', read_only=True)
    page = serializers.CharField()
    id = serializers.CharField()
    page_number = serializers.IntegerField()
    size = serializers.IntegerField()
    count = serializers.IntegerField()
    src = LikeSerializer(many=True)