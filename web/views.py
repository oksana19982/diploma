from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Comment, Image, Likes, Dislikes, CommentDislikes, CommentLikes
from .forms import CommentForm, ImageForm, SearchForm


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'web/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'web/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'web/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, args, kwargs)
        self.object.views += 1
        self.object.save()
        return response


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'web/post_search.html', {'title': 'About'})


def likes(request, post_pk):
    try:
        Likes.objects.create(
            user_id=request.user.id,
            post_id=post_pk,
        )
    except IntegrityError:
        pass
    return redirect('/post/%s' % post_pk)


def dislikes(request, post_pk):
    try:
        Dislikes.objects.create(
            user_id=request.user.id,
            post_id=post_pk,
        )
    except IntegrityError:
        pass
    return redirect('/post/%s' % post_pk)


def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('/post/%s' % post.pk)
    else:
        form = CommentForm()
    return render(request, 'web/comment_new.html', {'post': post, 'form': form, 'comment': comment})


def comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('/add_comment/%s' % post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'web/comment_edit.html', {'post': post, 'form': form, 'comment': comment})


def comment_likes(request, post_pk, comment_pk):
    try:
        CommentLikes.objects.create(
            user_id=request.user.id,
            comment_id=comment_pk,
        )
    except IntegrityError:
        pass
    return redirect('/post/%s' % post_pk)


def comment_dislikes(request, post_pk, comment_pk):
    try:
        CommentDislikes.objects.create(
            user_id=request.user.id,
            comment_id=comment_pk,
        )
    except IntegrityError:
        pass
    return redirect('/post/%s' % post_pk)


def image_upload_view(request, post_pk):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img_obj = form.instance
            img_obj.post_id = post_pk
            form.save()
            return redirect('/post/%s/update/' % post_pk)
    else:
        form = ImageForm()
    return render(request, 'web/index.html', {'form': form})


def latest_posts(request):
    latest_post = Post.objects.order_by('-date_posted')[:5]
    return render(request, 'web/latest_posts.html', {'latest_post': latest_post})


def networks(request):
    return render(request, 'web/networks.html', {'title': 'Networks'})


class AllUsers(ListView):
    model = User
    template_name = 'web/all_users.html'
    context_object_name = 'users'
    ordering = ['username']


def delete_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    post_id = image.post_id
    image.delete()
    return redirect('/post/%s/update/' % post_id)


def post_search(request):
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            posts = Post.objects.filter(title__icontains=cd['query'])
            return render(request, 'web/post_search.html', {'form': form, 'posts': posts})
    else:
        form = SearchForm()
    return render(request, 'web/post_search.html', {'form': form, 'posts': []})


def calendar(request):
    return render(request, 'web/calendar.html', {'title': 'calendar'})
