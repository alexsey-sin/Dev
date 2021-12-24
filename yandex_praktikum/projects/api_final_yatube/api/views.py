from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from rest_framework.permissions import IsAuthenticated
from .models import Group, Post, Follow
from .serializers import (
    GroupSerializer, PostSerializer,
    CommentSerializer, FollowSerializer
)
from .permissions import ReadOnly, IsOwnerOrReadOnly

User = get_user_model()


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        posts = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            posts = posts.filter(group=group)
        return posts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if post:
            serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_queryset(self):
        follow = self.queryset.filter(following=self.request.user)
        search_name = self.request.query_params.get('search', None)
        if search_name is not None:
            follow = follow.filter(user__username=search_name)
        return follow

    def perform_create(self, serializer):
        user = self.request.user
        follow_name = serializer.initial_data.get('following', None)
        if follow_name:
            following = get_object_or_404(User, username=follow_name)
            already = Follow.objects.filter(user=user, following=following).exists()
            if already or user == following:
                raise SuspiciousOperation('Bad request')
            else:
                serializer.save(user=user, following=following)
        else:
            raise SuspiciousOperation('Bad request')
