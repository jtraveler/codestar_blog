from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'