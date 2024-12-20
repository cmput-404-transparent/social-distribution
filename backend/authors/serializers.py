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
    relationship = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data
        """
        return Author.objects.create(**validated_data)
    
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

    def get_relationship(self, obj):
        """
        Get the relationship between the requesting user and the author being serialized.
        """

        if self.request_user:
            if self.request_user.id == obj.id:
                return 'SELF'
            
            if Follow.are_friends(self.request_user, obj):
                return 'FRIENDS'
            
            following = Follow.objects.filter(user=obj, follower=self.request_user)
            if following.exists():
                return Follow.objects.get(user=obj, follower=self.request_user).status
        
        return 'NONE'
    
    def get_followers(self, obj):
        """
        Get the number of followers for a user
        """
        return Follow.objects.filter(user=obj, status="FOLLOWED").count()
    
    def get_following(self, obj):
        """
        Get the number of followers for a user
        """
        return Follow.objects.filter(follower=obj, status="FOLLOWED").count()

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
        # instance.id = validated_data.get('id', instance.id)
        instance.save()
        return instance
    
    
class AuthorSummarySerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='author', read_only=True)
    id = serializers.SerializerMethodField()
    page = serializers.URLField()
    host = serializers.URLField()
    displayName = serializers.CharField(source='display_name')
    github = serializers.URLField(allow_blank=True, required=False)
    profileImage = serializers.URLField(source='profile_image', allow_blank=True, required=False)

    class Meta:
        model = Author
        fields = ['type', 'id', 'host', 'displayName', 'github', 'profileImage', 'page', 'fqid']

    def get_id(self, obj):
        return obj.fqid


    def get_url(self, obj):
        return self.get_id(obj)

class FollowRequestSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='follow', read_only=True)
    summary = serializers.SerializerMethodField()
    actor = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['type', 'summary', 'actor', 'object']
    
    def get_summary(self, obj):
        return f"{obj.follower.display_name} wants to follow {obj.user.display_name}"
    
    def get_actor(self, obj):
        return AuthorSummarySerializer(obj.follower).data
    
    def get_object(self, obj):
        return AuthorSummarySerializer(obj.user).data

