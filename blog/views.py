from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib import messages

def post_list(request):
    posts = Post.objects.all()
    search_term=''

    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = posts.filter(title__icontains = search_term)|posts.filter(text__icontains = search_term)

    return render(request, 'blog/post_list.html', {'posts': posts}, {'search_term':search_term})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    return render(request, 'blog/post_details.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk =pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def confirm_delete(request, pk):
    post = get_object_or_404(Post, pk =pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "This has been deleted")
        return redirect('post_list')
    return render(request, 'blog/confirm_delete.html', {'post':post})

