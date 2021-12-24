from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Group, Follow
from .forms import PostForm, CommentForm


User = get_user_model()


def index(request):
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page_number': page_number,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.text = form.cleaned_data['text']
        new_post.save()
        return redirect(reverse('index'))
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    if request.method == 'GET':
        following = False
        user = request.user
        # Найдем автора записей профиля
        author = get_object_or_404(User, username=username)
        user_is_author = author.id == user.id
        # Найдем все подписки пользователя если он авторизован
        if user.is_authenticated:
            following = user.follower.filter(author=author).count() == 1
        post_list = author.author_posts.all().order_by('-pub_date')
        count_posts = author.author_posts.count()
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {
            'author': author,
            'user': user,
            'page': page,
            'user_is_author': user_is_author,
            'following': following,
            'count_posts': count_posts,
        }
        return render(request, 'profile.html', context)
    return redirect(reverse('index'))


def post_view(request, username, post_id):
    if request.method == 'GET':
        user = request.user
        author = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        user_is_author = post.author == user
        count_posts = author.author_posts.count()
        form = CommentForm()
        context = {
            'author': author,
            'post': post,
            'comments': comments,
            'user_is_author': user_is_author,
            'count_posts': count_posts,
            'form': form,
        }
        return render(request, 'post.html', context)
    return redirect(reverse('index'))


@login_required
def post_edit(request, username, post_id):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user.id != author.id:
        return redirect('index')
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'GET':
        context = {'edit': True, 'form': form, 'post': post}
        return render(request, 'new_post.html', context)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse(
            'post', args=[f'{user.username}', f'{post_id}']))
    return redirect('index')


def page_not_found(request, exception):
    return render(
        request, 'misc/404.html', {'path': request.path}, status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    author_post = get_object_or_404(User, username=username)
    user = request.user
    form = CommentForm(request.POST or None)
    if request.method == 'GET':
        comments = post.comments.all()
        return render(request, 'comments.html',
                      {'form': form, 'comments': comments})
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = user
        comment.text = form.cleaned_data['text']
        comment.save()
        return redirect(reverse(
            'post', args=[f'{author_post.username}', f'{post_id}']))
    return redirect('index')


@login_required
def follow_index(request):
    follow = request.user.follower.all()
    authors = follow.values('author')
    post_list = Post.objects.filter(author__in=authors).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html',
                  {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        Follow.objects.get_or_create(user=user, author=author)
    return redirect(reverse('profile', args=[f'{author.username}']))


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=user, author=author).delete()
    return redirect(reverse('profile', args=[f'{author.username}']))
