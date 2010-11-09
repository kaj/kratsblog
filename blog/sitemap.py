from blog.models import Post
from django.contrib.sitemaps import Sitemap
from django.db.models import Max

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.6

    def items(self):
        return Post.objects.exclude(posted_time__exact=None)

    def lastmod(self, obj):
        return obj.posted_time

class RootSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.4
    
    def items(self):
        return ['/']

    def location(self, obj):
        return '/'

    def lastmod(self, obj):
        Post.objects.aggregate(mod=Max('posted_time'))['mod']

sitemaps = {
    'root': RootSitemap,
    'blog': BlogSitemap,
}
