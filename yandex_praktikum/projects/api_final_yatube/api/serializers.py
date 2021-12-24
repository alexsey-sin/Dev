from rest_framework import serializers
from .models import Group, Comment, Post, Follow


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'description')
        model = Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    group = serializers.ReadOnlyField(source='group.title')

    class Meta:
        fields = ('id', 'text', 'pub_date', 'group', 'author')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
