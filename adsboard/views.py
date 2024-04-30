from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from .models import Post, Comment
from .forms import CommentForm, PostForm
from .filters import PostFilter, CommentFilter


class PostList(ListView):
    model = Post
    ordering = "-post_time"
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
        return context

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentCreate(CreateView):
    model = Comment
    template_name = 'post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('comment_approval')
    
    def post(self, request, pk, **kwargs):
        comment_id = request.POST.get('comment_id')
        action = request.POST.get('action')
        if action == 'delete_comment':
            Comment.objects.get(id=comment_id).delete()
            return redirect('post_detail', pk=pk)

        else:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = Post.objects.get(pk=pk)
                new_comment.author = User.objects.get(username=request.user)
                new_comment.status = False
                new_comment.save()
            
            return redirect('comment_approval')


class CommentApproval(LoginRequiredMixin, ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'commentapproval.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(DetailView, CommentCreate):
    model = Post
    template_name = 'post_detail.html'

    def get(self, request, pk):
        context = {
            "comments" : Comment.objects.filter(post=Post.objects.get(pk=pk)).values('id','post_time',
                                                                                           'author__username',
                                                                                           'content', 'status').order_by('-post_time'),
            "OnePost" : Post.objects.get(pk=pk),
            'comment_form' : CommentForm,
        }

        return HttpResponse(render(request, 'post_detail.html', context))


class PostSearch(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'post_search.html'
    context_object_name = 'Post_search'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class MyPostList(ListView):
    model = Post
    ordering = "-post_time"
    template_name = 'mypost_list.html'
    paginate_by = 5

    def get(self, request):
        myposts = Post.objects.filter(author=User.objects.get(username=request.user))
        if len(myposts) == 0:
            context = {
                'No_posts': "_",
            }
        else:
            context = {
                'MyPosts': myposts,
                'posts_count' : len(myposts)
            }
        return HttpResponse(render(request, 'mypost_list.html', context))


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('classifiedads.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = "post_create.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): #
    permission_required = ('classifiedads.change_post',)
    model = Post
    form_class = PostForm
    raise_exception = True
    template_name = "post_edit.html"


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('classifiedads.delete_post',)
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy('post_list')


class CommentsList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'usercomments.html'
    context_object_name = 'usercomments'
    ordering = '-post_time'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        comments = Comment.objects.filter(post__author=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset=comments)
        return self.filterset.qs

    def post(self, request, *args, **kwargs):
        comment_id = request.POST['comment']
        comment = Comment.objects.get(id=comment_id)
        if comment.status:
            comment.status = False
        else:
            comment.status = True
        comment.save()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('/usercomments')
