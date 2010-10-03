from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from blog.models import Post

def index(request):
    posts = Post.objects.all()[:5]
    
    return direct_to_template(request, 'blog/index.html', {
            'posts': posts,
            })

def post_detail(request, year, month, slug):
    post = get_object_or_404(Post, 
                             posted_time__year=year, posted_time__month=month,
                             slug=slug)
    
    return direct_to_template(request, 'blog/post_detail.html', {
            'post': post,
            })
