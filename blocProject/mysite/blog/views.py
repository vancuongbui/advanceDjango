from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView)
from blog.models import Post, Comment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin   #for authentication
from django.contrib.auth.decorators import login_required   #for authentication as well
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy


# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'   #name the object and call it from html page
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        #where __lte = less than or equal from the above line of code
        #just like: Select * from Post where published_data <= time.zone.now()

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'      #name the object and call it from html page
    template_name = 'blog/post_detail.html'

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'blog/post_form.html'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Post
    form_class = PostForm
    redirect_field_name = 'blog/post_detail.html'    

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

#publication##################################################
@login_required()       #decorator
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
