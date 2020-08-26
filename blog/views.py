from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404  

def post_list(request):

    results = Post.objects.all()
    
    if request.method == 'GET':
        query= request.GET.get('search')
        submitbutton = request.GET.get('submit')
        
        if query is not None:
            lookups= Q(title__icontains=query) | Q(text__icontains=query)
            results= Post.objects.filter(lookups).distinct()
           

    context = {'submitbutton': submitbutton, 'results': results}

    return render (request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {'post': post, 'form': form}
    return render(request, 'blog/post_details.html', context)

@login_required
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

@login_required
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

@login_required
def confirm_delete(request, pk):
    post = get_object_or_404(Post, pk =pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "The post has been deleted")
        return redirect('post_list')
    return render(request, 'blog/confirm_delete.html', {'post':post})

@login_required
def comment_approve(request, pk):
    current_user = request.user
    comment = get_object_or_404(Comment, pk=pk)
    if current_user.is_superuser:
        comment.approve()
    else:
        raise Http404 
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    current_user = request.user
    comment = get_object_or_404(Comment, pk=pk)
    aux = comment.post.pk 
    if current_user.username == comment.author or current_user.is_superuser:
        if request.method == "POST":
            comment.delete()
            messages.success(request, "The comment has been deleted")
            return redirect ('post_detail', pk=comment.post.pk)
    else: 
        raise Http404
    context={'comment': comment, 'aux': aux}
    return render(request, 'blog/comment_remove.html', context)

@login_required
def profile_page(request):
    current_user = request.user
    return render(request, 'blog/profile_page.html', {'current_user': current_user})

@login_required
def delete_user(request):
    current_user = request.user
    if request.method == "POST":
        current_user.is_active = False
        current_user.save()
        messages.success(request, "The user has been deleted!")
        return redirect('post_list')
    return render(request, 'blog/confirm_user_delete.html', {"current_user": current_user})

