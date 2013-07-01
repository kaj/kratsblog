from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

from blog import views as blog
from blog import feeds
from blog.sitemap import sitemaps

urlpatterns = patterns(
    '',
    # Example:
    # (r'^kratsblog/', include('kratsblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', blog.index),
    url(r'^(?P<year>[0-9]{4})/$', blog.index),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', blog.index),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[a-z0-9-]+)',
        blog.post_detail),
    url(r'^node/(?P<id>[0-9]+)', blog.redirect_from_id),
    url(r'^atom\.xml', feeds.AtomFeed()),
    url(r'^rss.xml', feeds.RssFeed()),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', TemplateView.as_view( 
            template_name='robots.txt', content_type='text/plain')),
    url(r'^PIE\.htc$', TemplateView.as_view(
        template_name='PIE.htc', content_type='text/x-component')),
)

if settings.DEBUG and settings.MEDIA_URL[0] == '/':
    urlpatterns += patterns(
        '',
        url('500', TemplateView.as_view(template_name='500.html')),
        url('404', TemplateView.as_view(template_name='404.html')),
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 
         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
