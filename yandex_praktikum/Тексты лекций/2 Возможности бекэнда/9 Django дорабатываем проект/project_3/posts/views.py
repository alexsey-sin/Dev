from django.shortcuts import render

from .models import Post, User


def index(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts = Post.objects.select_related('author').select_related('group').filter(text__contains=keyword)
    else:
        posts = None

    return render(request, "index.html", {"posts": posts, "keyword": keyword})
