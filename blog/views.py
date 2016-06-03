from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.\
        filter(published_date__lte=timezone.now()).\
        order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required()
def post_drafts(request):
    posts = Post.objects.\
        filter(published_date__isnull=True).\
        order_by('creation_date')

    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required()
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.creation_date = timezone.now()
            post.author = request.user
            post.save()

            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'blog/post_new.html', {'form': form})
