from rest_framework import serializers
from .models import Post
import base64
from django.core.files.base import ContentFile
import commonmark
from .models import Post

import base64
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

Author = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'contentType', 'content', 'author', 'published', 'visibility']
        read_only_fields = ['id', 'authot', 'published']

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
