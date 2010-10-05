from django import template

from blog.models import Post

register = template.Library()

@register.inclusion_tag('blog/titles_by_month.html')
def titles_by_month():
    return {
        'posts' : Post.objects.all()
        }
