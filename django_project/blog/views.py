from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # django is looking for '<app>/<model>_<view type>.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  # ordering blog posts to display the newest first
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # django is looking for '<app>/<model>_<view type>.html'
    context_object_name = 'posts'
    paginate_by = 5

    # to modify the list that the query returns and just display posts for current user
    def get_queryset(self):
        # if user exists it will be captured in user variable - otherwise return 404
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


# this is a view with the form where users can create new posts
# to redirect to a home page after creating new post set attribute success_url in the CreateView to go to the home p
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #     set the fields for the form
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    #     set the fields for the form
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # make sure that a user who is updating is the one who created a post
    def test_func(self):
        post = self.get_object()  # get the post we're currently trying to update
        # check if the current user is the author of the post
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # after deleting post redirect user to a home page

    # make sure that a user who is deleting is the one who created a post
    def test_func(self):
        post = self.get_object()  # get the post we're currently trying to delete
        # check if the current user is the author of the post
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
