#  импортируйте в код всё необходимое
from .serializers import PostSerializer
from django.http import JsonResponse
from .models import Post


def get_post(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
    return JsonResponse(data=serializer.data)
