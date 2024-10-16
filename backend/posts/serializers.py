from rest_framework import serializers
from .models import Post, Author
import base64
from django.core.files.base import ContentFile

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'username', 'display_name', 'host', 'github', 'profile_image', 'page']
        read_only_fields = ['id']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'contentType', 'content', 'author', 'published', 'visibility']
        read_only_fields = ['id', 'author', 'published']

    def validate(self, data):
        if data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            try:
                base64.b64decode(data['content'])
            except Exception:
                raise serializers.ValidationError("Invalid base64 content for image.")
        return data

    def create(self, validated_data):
        if validated_data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')
            ext = format.split('/')[-1]
            validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"post_image_{validated_data['id']}.{ext}")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('contentType') in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')
            ext = format.split('/')[-1]
            validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"post_image_{instance.id}.{ext}")
        return super().update(instance, validated_data)