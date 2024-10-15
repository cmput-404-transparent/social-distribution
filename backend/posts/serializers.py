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



