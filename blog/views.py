# -*- encoding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from blog.models import Post
from django.template import defaultfilters
from datetime import datetime

def index(request, year=None, month=None):
    if year:
        all_posts = Post.objects.order_by('posted_time')
        if month:
            head = u'Tygbittar från %s' % (
               defaultfilters.date(datetime(int(year), int(month), 1), arg='F Y'))
            posts = get_list_or_404(all_posts, posted_time__year=year,
                                    posted_time__month=month)
        else:
            head = u'Tygbittar från %s' % year
            posts = get_list_or_404(all_posts, posted_time__year=year)
    else:
        head = None
        posts = Post.objects.exclude(posted_time__exact=None)[:5]
    
    return direct_to_template(request, 'blog/index.html', {
            'head': head,
            'posts': posts,
            'years': [x.year for x
                      in Post.objects.dates('posted_time', 'year')],
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
    posts = Post.objects.exclude(posted_time__exact=None),
    return redirect(get_object_or_404(posts, id=id),
                    permanent=True)
