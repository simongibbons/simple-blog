from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post


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

    return render(request, 'blog/post_list.html', {'posts' : posts})
