from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# The above is a functional view, the below is the same in Class Based View


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    # we need to tell django to pass the data as the variable 'posts' that we use in the template
    context_object_name = 'posts'
    # by default, it will show oldest to newest; but tu reverse it, add a minus(-) sign in front
    ordering = ['-date_posted']
    # The number below denotes how many posts/objects do you want per page
    # URLs and everything is set up by Django in backend - Already passes the context as well - edit in the template only
    # Try /?page=2
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    # Since we are overidng the query, our ordering will also be overwritten. So we have to order_by in the get_query_set
    paginate_by = 5

    # Overiding the below method so we can filter the posts with username
    def get_queryset(self):
        # If user doesn't exist, return 404; or else, get object
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # overriding formvalid method to add the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # overriding formvalid method to add the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # A function to check if the logged in user is the author or not. Uses the UserPassesTestMixin
    def test_func(self):
        # getting the post that we are currently updating
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # A function to check if the logged in user is the author or not. Uses the UserPassesTestMixin
    def test_func(self):
        # getting the post that we are currently updating
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
