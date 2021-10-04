from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Posts
from django.views.generic import ListView , DetailView ,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.


def home(request):
    context = {
        'posts' : Posts.objects.all()
    }
    return render(request,'blogapp/home.html',context)


class PostListView(ListView):
    model = Posts
    template_name = 'blogapp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Posts
    template_name = 'blogapp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username = self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Posts
    template_name = 'blogapp/post_detail.html'


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Posts
    fields = ['title','content']
    template_name = 'blogapp/post_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView ):
    model = Posts 
    fields = ['title','content']
    template_name = 'blogapp/post_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Posts
    template_name = 'blogapp/post_confirm_delete.html'
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'blogapp/about.html')