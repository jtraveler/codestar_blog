from django.shortcuts import render
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_on')