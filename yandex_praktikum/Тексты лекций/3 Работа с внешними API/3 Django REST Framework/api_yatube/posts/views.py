from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer, CommentSerializer
from .permissions import ReadOnly, IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | ReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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
