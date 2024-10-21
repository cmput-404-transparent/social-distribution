from rest_framework import serializers
from .models import *


class AuthorSerializer(serializers.Serializer):
    type = serializers.CharField(default='author', read_only=True)
    host = serializers.URLField()
    display_name = serializers.CharField()
    github = serializers.URLField()
    profile_image = serializers.URLField()
    page = serializers.URLField()
    username = serializers.CharField()
    display_name = serializers.CharField()
    id = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data
        """
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Author` instance, given the validated data
        """
        instance.host = validated_data.get('host', instance.host)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.github = validated_data.get('github', instance.github)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.page = validated_data.get('page', instance.page)
        instance.username = validated_data.get('username', instance.username)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.id = validated_data.get('id', instance.id)
        instance.save()
        return instance
    
    
class AuthorSummarySerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='author', read_only=True)
    id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    host = serializers.URLField()
    displayName = serializers.CharField(source='display_name')
    github = serializers.URLField(allow_blank=True, required=False)
    profileImage = serializers.URLField(source='profile_image', allow_blank=True, required=False)

    class Meta:
        model = Author
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage']

    def get_id(self, obj):
        return f"{obj.host}authors/{obj.id}/"

    def get_url(self, obj):
        return self.get_id(obj)
