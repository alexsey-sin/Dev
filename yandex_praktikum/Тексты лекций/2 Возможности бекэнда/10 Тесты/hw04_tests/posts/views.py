from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
# from django.views.decorators.cache import cache_page

from .models import Post, Group
from .forms import PostForm, CommentForm


User = get_user_model()


def index(request):
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'page_number': page_number,
    }
    return render(request, 'index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')[:12]
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.text = form.cleaned_data['text']
        new_post.save()
        return redirect(reverse('index'))
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    if request.method == 'GET':
        user_is_author = False
        user = request.user
        author = get_object_or_404(User, username=username)
        if author.id == user.id:
            user_is_author = True
        post_list = author.author_posts.all().order_by('-pub_date')
        count_posts = author.author_posts.count()
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {
            'author': author,
            'page': page,
            'user_is_author': user_is_author,
            'count_posts': count_posts,
        }
        return render(request, 'profile.html', context)
    return redirect(reverse('index'))


def post_view(request, username, post_id):
    if request.method == 'GET':
        user_is_author = False
        user = request.user
        author = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        if post.author_id == user.id:
            user_is_author = True
        count_posts = author.author_posts.count()
        context = {
            'author': author,
            'post': post,
            'comments': comments,
            'user_is_author': user_is_author,
            'count_posts': count_posts,
        }
        return render(request, 'post.html', context)
    return redirect(reverse('index'))


@login_required
def post_edit(request, username, post_id):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user.id != author.id:
        return redirect('index')
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id)
        form = PostForm({
            'text': post.text,
            'group': post.group_id,
        })
        return render(request, 'new_post.html', {'edit': True, 'form': form})
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST,
                        files=request.FILES or None, instance=post)
        if form.is_valid():
            edit_post = form.save(commit=False)
            edit_post.text = form.cleaned_data['text']
            edit_post.save()
            return redirect(reverse(
                'post', args=[f'{user.username}', f'{post_id}']))
    return redirect('index')


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    author_post = get_object_or_404(User, username=username)
    user = request.user
    if request.method == 'GET':
        comments = post.comments.all()
        form = CommentForm()
        return render(request, 'comments.html', {'form': form, 'comments': comments})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect(reverse(
                'post', args=[f'{author_post.username}', f'{post_id}']))
    return redirect('index')
