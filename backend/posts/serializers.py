from rest_framework import serializers
from .models import Post

import base64
from django.core.files.base import ContentFile


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'contentType', 'content', 'author', 'published']

        #read_only_fields = ['author', 'published']


        # !!!!!!!!!!!   IMAGE --- DOUBT -- GPT 

        def validate(self, data):
        # If contentType is for image, ensure content is valid base64
            if data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
                try:
                    base64.b64decode(data['content'])
                except Exception:
                    raise serializers.ValidationError("Invalid base64 content for image.")
            return data

        def create(self, validated_data):
            if validated_data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
                # Handle base64 image
                format, imgstr = validated_data['content'].split(';base64,')  # Split base64 string
                ext = format.split('/')[-1]  # Get extension (png or jpeg)
                validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

            return super().create(validated_data)

        def update(self, instance, validated_data):
            if validated_data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
                format, imgstr = validated_data['content'].split(';base64,')
                ext = format.split('/')[-1]
                validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

            return super().update(instance, validated_data)








from rest_framework import serializers
from .models import Post
import base64
from django.core.files.base import ContentFile

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False)
    contentType = serializers.ChoiceField(choices=[
        ('text/plain', 'Plain Text'),
        ('text/markdown', 'Markdown'),
        ('image/png;base64', 'PNG Image'),
        ('image/jpeg;base64', 'JPEG Image')
    ], default='text/plain')
    content = serializers.CharField()
    author = serializers.IntegerField()  # We'll map this to the `User` model later
    published = serializers.DateTimeField()

    def validate(self, data):
        # If contentType is for image, ensure content is valid base64
        if data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
            try:
                base64.b64decode(data['content'])
            except Exception:
                raise serializers.ValidationError("Invalid base64 content for image.")
        return data

    def create(self, validated_data):
        # Handle base64 image content if applicable
        if validated_data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')  # Split base64 string
            ext = format.split('/')[-1]  # Get extension (png or jpeg)
            validated_data['content'] = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        # Create a new Post instance
        author_id = validated_data.pop('author')  # Extract author_id
        validated_data['author_id'] = author_id  # Map to the foreign key
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update the instance fields with the new data
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.content = validated_data.get('content', instance.content)
        instance.published = validated_data.get('published', instance.published)

        # Handle base64 image content if applicable
        if validated_data['contentType'] in ['image/png;base64', 'image/jpeg;base64']:
            format, imgstr = validated_data['content'].split(';base64,')
            ext = format.split('/')[-1]
            instance.content = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")

        instance.save()
        return instance
