from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context_group = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, "posts/group_list.html", context_group)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    count = user.posts.order_by('-pub_date').count()
    posts = user.posts.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context_profile = {
        'user': user,
        'count': count,
        'page_obj': page_obj,
    }

    return render(request, "posts/profile.html", context_profile)


def post_detail(request, post_id):
    post_valid = get_object_or_404(Post, id=post_id)
    post_obj = Post.objects.get(id=post_id)
    usser = get_object_or_404(User, username=post_obj.author.username)
    count = usser.posts.order_by('-pub_date').count()
    context_detail = {
        'post_valid': post_valid,
        'post_obj': post_obj,
        'usser': usser,
        'count': count,
        'post_id': post_id,
    }

    return render(request, "posts/post_detail.html", context_detail)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('posts:profile', username=request.user.username)
        return render(request, "posts/create_post.html", {'form': form})
    form = PostForm()
    return render(request, "posts/create_post.html", {'form': form})


def post_edit(request, post_id):
    post_obj = Post.objects.get(id=post_id)
    usser = get_object_or_404(User, username=post_obj.author.username)
    if request.user == usser:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post_obj)
            if form.is_valid():
                form.author = request.user
                form.save()
            return render(
                request,
                "posts/create_post.html",
                {'is_edit': True, 'form': form, },
            )
        form = PostForm(instance=post_obj)
        return render(
            request,
            "posts/create_post.html",
            {'is_edit': True, 'form': form, },
        )
    return redirect(
        'posts:post_detail',
        post_id=post_id,
    )
