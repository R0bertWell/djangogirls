from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import PostForm


def post_list(request, author=None):
    if author:
        author_id = get_object_or_404(User, pk=author)
        posts = Post.objects.filter(author=author_id).order_by('published_date')
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post, 'posts': posts})


def post_edit(request, pk):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.author == request.user:
                post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post, 'posts': posts})


def post_new(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form, 'posts': posts})
