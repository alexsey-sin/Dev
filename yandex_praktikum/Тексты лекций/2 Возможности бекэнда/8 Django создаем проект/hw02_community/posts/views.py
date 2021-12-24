from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    latest = Post.objects.order_by('-pub_date')[:11]
    response = render(request, 'index.html', {'posts': latest})
    return response


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:12]
    response = render(request, 'group.html',
                      {'group': group, 'posts': posts})
    return response
