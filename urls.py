from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.views.static import serve
admin.autodiscover()

from blog import views as blog
from blog import feeds
from blog.sitemap import sitemaps

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', blog.index),
    url(r'^(?P<year>[0-9]{4})/$', blog.index),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', blog.index),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[a-z0-9-]+)',
        blog.post_detail),
    url(r'^node/(?P<id>[0-9]+)', blog.redirect_from_id),
    url(r'^atom\.xml', feeds.AtomFeed()),
    url(r'^rss.xml', feeds.RssFeed()),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', TemplateView.as_view( 
            template_name='robots.txt', content_type='text/plain')),
    url(r'^PIE\.htc$', TemplateView.as_view(
        template_name='PIE.htc', content_type='text/x-component')),
]

if settings.DEBUG and settings.MEDIA_URL[0] == '/':
    urlpatterns += [
        url('500', TemplateView.as_view(template_name='500.html')),
        url('404', TemplateView.as_view(template_name='404.html')),
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
            serve, {'document_root': settings.MEDIA_ROOT}),
    ]
