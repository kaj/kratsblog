from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from blog.models import Post

def index(request, year=None, month=None):
    if year:
        if month:
            posts = get_list_or_404(Post, posted_time__year=year,
                                    posted_time__month=month)
        else:
            posts = get_list_or_404(Post, posted_time__year=year)
    else:
        posts = Post.objects.all()[:5]
    # TODO Fix this with an annotation?
    for post in posts:
        if post.image_set.all().count():
            post.ximg = post.image_set.all()[0]
        else:
            post.ximg = None
    
    return direct_to_template(request, 'blog/index.html', {
            'posts': posts,
            })

def post_detail(request, year, month, slug):
    post = get_object_or_404(Post, 
                             posted_time__year=year, posted_time__month=month,
                             slug=slug)
    
    return direct_to_template(request, 'blog/post_detail.html', {
            'post': post,
            'images': post.image_set.all,
            })

def redirect_from_id(request, id):
    return redirect(get_object_or_404(Post, id=id))
