from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

from .models import Post
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.\
        filter(published_date__lte=timezone.now()).\
        order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.is_published() and not request.user.is_authenticated():
        raise Http404('Unauthorized users cannot view unpublished posts')

    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


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
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'blog/post_new.html', {'form': form})

@login_required()
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.publish()
        return redirect(post)
    else:
        # Only accept post requests on this view
        return HttpResponse(status=204)


@login_required()
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('/')
    else:
        return HttpResponse(status=204)

@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_new.html', {'form': form})

def post_add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

    return redirect(post)
